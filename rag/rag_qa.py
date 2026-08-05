import gc
import json
import math
import time
import urllib.request
from pathlib import Path

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler


# RAGで参照するMarkdown文書
SOURCE_PATH = Path("notes/day14_api_summary.md")

# 今回は500文字に固定し、検索上位3件をモデルへ渡す
CHUNK_SIZE = 500
TOP_K = 3

# 文書と質問のEmbeddingには、Ollama上のbge-m3を使う
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"

# TinySwallowはOllamaのChat API経由で呼び出す
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = (
    "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M"
)

# EvoLLM-JPとRLT-7Bは、ローカルのMLXモデルを読み込む
MLX_MODELS = {
    "EvoLLM-JP-v1-7B": Path(
        "models/EvoLLM-JP-v1-7B-4bit"
    ),
    "RLT-7B": Path("models/RLT-7B-4bit"),
}

# 比較条件を揃えるため、全モデルで同じ生成上限を使う
MAX_TOKENS = 500

# 3モデルへ共通で与える役割と制約
SYSTEM_PROMPT = """
あなたは、与えられた根拠だけを使って質問に答えるアシスタントです。
根拠に答えがない場合は、推測せず「根拠からは分かりません」と答えてください。
日本語で簡潔に回答してください。
""".strip()


def split_by_size(text, chunk_size):
    """文章を指定した文字数ごとに分割する。"""

    return [
        text[start:start + chunk_size]
        for start in range(0, len(text), chunk_size)
    ]


def embed(texts):
    """文章をbge-m3へ送り、Embeddingの一覧を取得する。"""

    data = json.dumps({
        "model": EMBED_MODEL,
        "input": texts,
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(
        request,
        timeout=300,
    ) as response:
        result = json.load(response)

    return result["embeddings"]


def cosine_similarity(vector_a, vector_b):
    """2つのベクトルの向きがどれくらい近いか計算する。"""

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )
    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


def search_chunks(query, chunks, top_k):
    """質問に近いチャンクを、類似度が高い順に返す。"""

    # 質問と全チャンクをそれぞれベクトル化する
    query_vector = embed([query])[0]
    chunk_vectors = embed(chunks)

    search_results = []

    # 質問と各チャンクの類似度を計算する
    for index, (chunk, chunk_vector) in enumerate(
        zip(chunks, chunk_vectors),
        start=1,
    ):
        score = cosine_similarity(
            query_vector,
            chunk_vector,
        )

        search_results.append({
            "index": index,
            "score": score,
            "text": chunk,
        })

    # 類似度が高い順に並べ、指定件数だけ返す
    search_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return search_results[:top_k]


def build_rag_prompt(query, search_results):
    """検索結果を、全モデル共通のRAGプロンプトへ組み込む。"""

    context_parts = []

    # 各チャンクへ番号を付け、根拠を区別できる形にする
    for rank, result in enumerate(
        search_results,
        start=1,
    ):
        context_parts.append(
            f"[根拠{rank}]\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    return f"""
以下の根拠だけを使って質問に答えてください。

{context}

[質問]
{query}
""".strip()


def answer_with_ollama(rag_prompt):
    """TinySwallowへ質問し、回答と所要時間を返す。"""

    data = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": rag_prompt,
            },
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": MAX_TOKENS,
        },
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    # API送信から回答受信までの時間を測る
    started_at = time.perf_counter()

    with urllib.request.urlopen(
        request,
        timeout=300,
    ) as response:
        result = json.load(response)

    elapsed = time.perf_counter() - started_at

    return result["message"]["content"], elapsed


def answer_with_mlx(model_path, rag_prompt):
    """MLXモデルへ質問し、回答と所要時間を返す。"""

    # モデル読み込み時間も含めて計測する
    started_at = time.perf_counter()

    model, tokenizer = load(str(model_path))

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": rag_prompt,
        },
    ]

    # モデルごとの会話形式へプロンプトを変換する
    if getattr(tokenizer, "chat_template", None):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    else:
        # 会話テンプレートがない場合の予備処理
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"{rag_prompt}\n\n"
            "回答:"
        )

    # 回答の揺れを抑えるため、低いtemperatureを使う
    sampler = make_sampler(temp=0.1)

    answer = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=MAX_TOKENS,
        sampler=sampler,
        verbose=False,
    )

    elapsed = time.perf_counter() - started_at

    # 次のモデルを読み込む前にメモリを解放する
    del model
    del tokenizer
    gc.collect()
    mx.clear_cache()

    return answer, elapsed


def print_search_results(search_results):
    """モデルへ渡す検索結果を確認用に表示する。"""

    print("\n" + "=" * 70)
    print("検索された根拠")
    print("=" * 70)

    for rank, result in enumerate(
        search_results,
        start=1,
    ):
        # 改行を空白へ変え、先頭240文字を表示する
        normalized_text = " ".join(
            result["text"].split()
        )
        preview = normalized_text[:240]

        if len(normalized_text) > 240:
            preview += " ..."

        print(
            f"\n{rank}位 | "
            f"チャンク{result['index']} | "
            f"スコア {result['score']:.4f}"
        )
        print(preview)


def main():
    """検索から3モデルの回答比較までを実行する。"""

    # 必要な文書とMLXモデルが存在するか先に確認する
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            f"参照文書がありません: {SOURCE_PATH}"
        )

    for model_name, model_path in MLX_MODELS.items():
        if not model_path.exists():
            raise FileNotFoundError(
                f"{model_name}がありません: {model_path}"
            )

    # 文書を読み込み、500文字ずつに分割する
    text = SOURCE_PATH.read_text(encoding="utf-8")
    chunks = split_by_size(text, CHUNK_SIZE)

    query = input("質問を入力してください: ").strip()

    if not query:
        print("質問が空なので終了します。")
        return

    print(f"\n参照文書: {SOURCE_PATH}")
    print(f"チャンクサイズ: {CHUNK_SIZE}文字")
    print(f"チャンク数: {len(chunks)}")
    print(f"検索件数: 上位{TOP_K}件")

    # 質問に近いチャンクを検索する
    search_results = search_chunks(
        query,
        chunks,
        TOP_K,
    )

    print_search_results(search_results)

    # 同じ検索結果から共通プロンプトを作る
    rag_prompt = build_rag_prompt(
        query,
        search_results,
    )

    # TinySwallowをOllama経由で呼ぶ
    print("\n" + "=" * 70)
    print("TinySwallow / Ollama")
    print("=" * 70)

    answer, elapsed = answer_with_ollama(rag_prompt)

    print(answer)
    print(f"\n所要時間: {elapsed:.2f}秒")

    # MLXモデルを1本ずつ読み込み、同じ質問へ回答させる
    for model_name, model_path in MLX_MODELS.items():
        print("\n" + "=" * 70)
        print(f"{model_name} / MLX")
        print("=" * 70)

        answer, elapsed = answer_with_mlx(
            model_path,
            rag_prompt,
        )

        print(answer)
        print(f"\n所要時間: {elapsed:.2f}秒")


if __name__ == "__main__":
    main()