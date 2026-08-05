"""Day20: RLT-7BでRAGなし／ありの回答を比較する。"""

import gc
import json
import math
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler


# 評価条件を固定し、RAGの有無以外をできるだけ揃える
MATERIALS_PATH = Path("eval/materials.md")
MODEL_PATH = Path("models/RLT-7B-4bit")
WITHOUT_RAG_PATH = Path("eval/runs/day20_rag_without.md")
WITH_RAG_PATH = Path("eval/runs/day20_rag_with.md")

CHUNK_SIZE = 500
TOP_K = 3
MAX_TOKENS = 500
TEMPERATURE = 0.1

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"

SYSTEM_PROMPT = """
あなたは質問に日本語で簡潔に回答するアシスタントです。
分からない情報を推測で補わず、分からない場合はそのことを明記してください。
""".strip()

QUESTIONS = [
    {
        "id": "Q7",
        "title": "FAQ回答",
        "query": (
            "TaskBridgeについて、無料トライアル中に招待できる人数と、"
            "トライアル終了後のデータの扱いを教えてください。"
        ),
    },
    {
        "id": "Q9",
        "title": "矛盾検出",
        "query": (
            "問い合わせ分類AIの初期仕様について、"
            "矛盾または確認が必要な点を指摘してください。"
        ),
    },
]


def split_by_size(text, chunk_size):
    """素材を指定文字数ごとの検索単位へ分割する。"""

    return [
        text[start:start + chunk_size]
        for start in range(0, len(text), chunk_size)
    ]


def embed(texts):
    """Ollamaのbge-m3で文章をEmbeddingへ変換する。"""

    data = json.dumps({
        "model": EMBED_MODEL,
        "input": texts,
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.load(response)

    return result["embeddings"]


def cosine_similarity(vector_a, vector_b):
    """2つのEmbeddingのコサイン類似度を計算する。"""

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


def search_chunks(query, chunks, chunk_vectors):
    """質問に近いチャンクを上位TOP_K件返す。"""

    query_vector = embed([query])[0]
    results = []

    for index, (chunk, chunk_vector) in enumerate(
        zip(chunks, chunk_vectors),
        start=1,
    ):
        results.append({
            "index": index,
            "score": cosine_similarity(
                query_vector,
                chunk_vector,
            ),
            "text": chunk,
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )
    return results[:TOP_K]


def build_prompt(query, search_results=None):
    """RAGなし、または検索根拠付きのプロンプトを作る。"""

    if search_results is None:
        return query

    context_parts = []
    for rank, result in enumerate(search_results, start=1):
        context_parts.append(
            f"[根拠{rank}]\n{result['text']}"
        )

    context = "\n\n".join(context_parts)
    return f"""
以下の根拠だけを使って質問に答えてください。
根拠に答えがない場合は、推測せず「根拠からは分かりません」と答えてください。

{context}

[質問]
{query}
""".strip()


def answer(model, tokenizer, user_prompt):
    """読み込み済みのRLT-7Bで回答し、生成時間を返す。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    if getattr(tokenizer, "chat_template", None):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    else:
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"{user_prompt}\n\n回答:"
        )

    sampler = make_sampler(temp=TEMPERATURE)
    started_at = time.perf_counter()
    generated_text = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=MAX_TOKENS,
        sampler=sampler,
        verbose=False,
    )
    elapsed = time.perf_counter() - started_at

    return generated_text, elapsed


def format_without_rag(results, model_load_seconds):
    """RAGなしの回答をMarkdownへ整形する。"""

    lines = [
        "# Day20 RAGなし評価出力",
        "",
        f"- 実行日時: {datetime.now().isoformat(timespec='seconds')}",
        "- モデル: RLT-7B 4bit / MLX",
        f"- モデル読み込み時間: {model_load_seconds:.2f}秒",
        f"- temperature: {TEMPERATURE}",
        f"- max_tokens: {MAX_TOKENS}",
    ]

    for result in results:
        lines.extend([
            "",
            f"## {result['id']}. {result['title']}",
            "",
            "### 質問",
            "",
            result["query"],
            "",
            "### 回答",
            "",
            result["answer"],
            "",
            f"生成時間: {result['elapsed']:.2f}秒",
        ])

    return "\n".join(lines) + "\n"


def format_with_rag(results, model_load_seconds):
    """RAGありの検索結果と回答をMarkdownへ整形する。"""

    lines = [
        "# Day20 RAGあり評価出力",
        "",
        f"- 実行日時: {datetime.now().isoformat(timespec='seconds')}",
        "- モデル: RLT-7B 4bit / MLX",
        f"- モデル読み込み時間: {model_load_seconds:.2f}秒",
        f"- 参照資料: {MATERIALS_PATH}",
        f"- チャンクサイズ: {CHUNK_SIZE}文字",
        f"- 検索件数: 上位{TOP_K}件",
        f"- Embeddingモデル: {EMBED_MODEL}",
        f"- temperature: {TEMPERATURE}",
        f"- max_tokens: {MAX_TOKENS}",
    ]

    for result in results:
        lines.extend([
            "",
            f"## {result['id']}. {result['title']}",
            "",
            "### 質問",
            "",
            result["query"],
            "",
            "### 検索結果",
        ])

        for rank, search_result in enumerate(
            result["search_results"],
            start=1,
        ):
            lines.extend([
                "",
                (
                    f"#### {rank}位: チャンク"
                    f"{search_result['index']} "
                    f"(類似度 {search_result['score']:.4f})"
                ),
                "",
                search_result["text"],
            ])

        lines.extend([
            "",
            "### 回答",
            "",
            result["answer"],
            "",
            f"生成時間: {result['elapsed']:.2f}秒",
        ])

    return "\n".join(lines) + "\n"


def main():
    """Q7・Q9をRAGなし／ありで実行して保存する。"""

    if not MATERIALS_PATH.exists():
        raise FileNotFoundError(
            f"評価素材がありません: {MATERIALS_PATH}"
        )
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"RLT-7Bがありません: {MODEL_PATH}"
        )

    # 素材のEmbeddingは一度だけ作り、両方の質問で再利用する
    materials = MATERIALS_PATH.read_text(encoding="utf-8")
    chunks = split_by_size(materials, CHUNK_SIZE)
    print(f"評価素材を{len(chunks)}チャンクへ分割しました。")
    chunk_vectors = embed(chunks)

    print("RLT-7Bを読み込んでいます...")
    load_started_at = time.perf_counter()
    model, tokenizer = load(str(MODEL_PATH))
    model_load_seconds = time.perf_counter() - load_started_at
    print(f"読み込み完了: {model_load_seconds:.2f}秒")

    without_rag_results = []
    with_rag_results = []

    for question in QUESTIONS:
        print(f"\n{question['id']} RAGなしを生成しています...")
        generated_text, elapsed = answer(
            model,
            tokenizer,
            question["query"],
        )
        without_rag_results.append({
            **question,
            "answer": generated_text,
            "elapsed": elapsed,
        })
        print(f"完了: {elapsed:.2f}秒")

        print(f"{question['id']} RAGありを生成しています...")
        search_results = search_chunks(
            question["query"],
            chunks,
            chunk_vectors,
        )
        rag_prompt = build_prompt(
            question["query"],
            search_results,
        )
        generated_text, elapsed = answer(
            model,
            tokenizer,
            rag_prompt,
        )
        with_rag_results.append({
            **question,
            "search_results": search_results,
            "answer": generated_text,
            "elapsed": elapsed,
        })
        print(f"完了: {elapsed:.2f}秒")

    WITHOUT_RAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    WITHOUT_RAG_PATH.write_text(
        format_without_rag(
            without_rag_results,
            model_load_seconds,
        ),
        encoding="utf-8",
    )
    WITH_RAG_PATH.write_text(
        format_with_rag(
            with_rag_results,
            model_load_seconds,
        ),
        encoding="utf-8",
    )

    del model
    del tokenizer
    gc.collect()
    mx.clear_cache()

    print("\n評価結果を保存しました。")
    print(f"RAGなし: {WITHOUT_RAG_PATH}")
    print(f"RAGあり: {WITH_RAG_PATH}")


if __name__ == "__main__":
    main()
