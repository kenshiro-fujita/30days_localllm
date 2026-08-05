"""Day20: Q9をTinySwallowとEvoLLM-JPで追加比較する。"""

import gc
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import mlx.core as mx
from mlx_lm import load

from run_day20_rag_eval import (
    CHUNK_SIZE,
    MAX_TOKENS,
    MATERIALS_PATH,
    SYSTEM_PROMPT,
    TEMPERATURE,
    answer,
    build_prompt,
    embed,
    search_chunks,
    split_by_size,
)


OUTPUT_PATH = Path("eval/runs/day20_q9_model_compare.md")
EVO_MODEL_PATH = Path("models/EvoLLM-JP-v1-7B-4bit")

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
TINY_MODEL = (
    "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M"
)

QUESTION = {
    "id": "Q9",
    "title": "矛盾検出",
    "query": (
        "問い合わせ分類AIの初期仕様について、"
        "矛盾または確認が必要な点を指摘してください。"
    ),
}


def answer_with_tiny(user_prompt):
    """Ollama経由でTinySwallowの回答と生成時間を取得する。"""

    data = json.dumps({
        "model": TINY_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS,
        },
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    started_at = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.load(response)
    elapsed = time.perf_counter() - started_at

    return result["message"]["content"], elapsed


def run_tiny(without_prompt, rag_prompt):
    """TinySwallowでRAGなし／ありを順番に実行する。"""

    print("TinySwallow: RAGなしを生成しています...")
    without_answer, without_elapsed = answer_with_tiny(
        without_prompt
    )
    print(f"完了: {without_elapsed:.2f}秒")

    print("TinySwallow: RAGありを生成しています...")
    with_answer, with_elapsed = answer_with_tiny(rag_prompt)
    print(f"完了: {with_elapsed:.2f}秒")

    return {
        "model": "TinySwallow 1.5B Q5_K_M / Ollama",
        "model_load_seconds": None,
        "without_answer": without_answer,
        "without_elapsed": without_elapsed,
        "with_answer": with_answer,
        "with_elapsed": with_elapsed,
    }


def run_evo(without_prompt, rag_prompt):
    """EvoLLM-JPでRAGなし／ありを順番に実行する。"""

    print("EvoLLM-JPを読み込んでいます...")
    load_started_at = time.perf_counter()
    model, tokenizer = load(str(EVO_MODEL_PATH))
    model_load_seconds = time.perf_counter() - load_started_at
    print(f"読み込み完了: {model_load_seconds:.2f}秒")

    print("EvoLLM-JP: RAGなしを生成しています...")
    without_answer, without_elapsed = answer(
        model,
        tokenizer,
        without_prompt,
    )
    print(f"完了: {without_elapsed:.2f}秒")

    print("EvoLLM-JP: RAGありを生成しています...")
    with_answer, with_elapsed = answer(
        model,
        tokenizer,
        rag_prompt,
    )
    print(f"完了: {with_elapsed:.2f}秒")

    del model
    del tokenizer
    gc.collect()
    mx.clear_cache()

    return {
        "model": "EvoLLM-JP-v1-7B 4bit / MLX",
        "model_load_seconds": model_load_seconds,
        "without_answer": without_answer,
        "without_elapsed": without_elapsed,
        "with_answer": with_answer,
        "with_elapsed": with_elapsed,
    }


def format_markdown(results, search_results):
    """モデルごとの全文回答と共通検索結果をMarkdown化する。"""

    lines = [
        "# Day20 Q9 モデル比較",
        "",
        f"- 実行日時: {datetime.now().isoformat(timespec='seconds')}",
        f"- 質問: {QUESTION['query']}",
        f"- temperature: {TEMPERATURE}",
        f"- max_tokens: {MAX_TOKENS}",
        f"- チャンクサイズ: {CHUNK_SIZE}文字",
        "- RAGありの検索結果: 全モデルで共通",
        "",
        "## 共通の検索結果",
    ]

    for rank, search_result in enumerate(search_results, start=1):
        lines.extend([
            "",
            (
                f"### {rank}位: チャンク"
                f"{search_result['index']} "
                f"(類似度 {search_result['score']:.4f})"
            ),
            "",
            search_result["text"],
        ])

    for result in results:
        lines.extend([
            "",
            f"## {result['model']}",
        ])
        if result["model_load_seconds"] is not None:
            lines.extend([
                "",
                (
                    "モデル読み込み時間: "
                    f"{result['model_load_seconds']:.2f}秒"
                ),
            ])
        lines.extend([
            "",
            "### RAGなし",
            "",
            result["without_answer"],
            "",
            f"生成時間: {result['without_elapsed']:.2f}秒",
            "",
            "### RAGあり",
            "",
            result["with_answer"],
            "",
            f"生成時間: {result['with_elapsed']:.2f}秒",
        ])

    return "\n".join(lines) + "\n"


def main():
    """共通の検索結果を使って2モデルを比較する。"""

    if not MATERIALS_PATH.exists():
        raise FileNotFoundError(
            f"評価素材がありません: {MATERIALS_PATH}"
        )
    if not EVO_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"EvoLLM-JPがありません: {EVO_MODEL_PATH}"
        )

    materials = MATERIALS_PATH.read_text(encoding="utf-8")
    chunks = split_by_size(materials, CHUNK_SIZE)
    chunk_vectors = embed(chunks)
    search_results = search_chunks(
        QUESTION["query"],
        chunks,
        chunk_vectors,
    )

    without_prompt = QUESTION["query"]
    rag_prompt = build_prompt(
        QUESTION["query"],
        search_results,
    )

    results = [
        run_tiny(without_prompt, rag_prompt),
        run_evo(without_prompt, rag_prompt),
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        format_markdown(results, search_results),
        encoding="utf-8",
    )

    print(f"\n比較結果を保存しました: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
