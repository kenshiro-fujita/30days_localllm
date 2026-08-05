"""Day20: Q9へ検索1位だけを渡し、3モデルで比較する。"""

import gc
import time
from pathlib import Path

import mlx.core as mx
from mlx_lm import load

from run_day20_q9_model_compare import (
    QUESTION,
    format_markdown,
    run_evo,
    run_tiny,
)
from run_day20_rag_eval import (
    MATERIALS_PATH,
    MODEL_PATH,
    answer,
    build_prompt,
    embed,
    search_chunks,
    split_by_size,
    CHUNK_SIZE,
)


OUTPUT_PATH = Path("eval/runs/day20_q9_top1_compare.md")


def run_rlt(without_prompt, rag_prompt):
    """RLT-7BでRAGなし／検索1位だけのRAGありを実行する。"""

    print("RLT-7Bを読み込んでいます...")
    load_started_at = time.perf_counter()
    model, tokenizer = load(str(MODEL_PATH))
    model_load_seconds = time.perf_counter() - load_started_at
    print(f"読み込み完了: {model_load_seconds:.2f}秒")

    print("RLT-7B: RAGなしを生成しています...")
    without_answer, without_elapsed = answer(
        model,
        tokenizer,
        without_prompt,
    )
    print(f"完了: {without_elapsed:.2f}秒")

    print("RLT-7B: RAGあり（検索1位のみ）を生成しています...")
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
        "model": "RLT-7B 4bit / MLX",
        "model_load_seconds": model_load_seconds,
        "without_answer": without_answer,
        "without_elapsed": without_elapsed,
        "with_answer": with_answer,
        "with_elapsed": with_elapsed,
    }


def main():
    """検索1位だけを共通根拠として3モデルを比較する。"""

    materials = MATERIALS_PATH.read_text(encoding="utf-8")
    chunks = split_by_size(materials, CHUNK_SIZE)
    chunk_vectors = embed(chunks)

    # search_chunksは上位3件を返すため、先頭の1件だけに絞る
    search_results = search_chunks(
        QUESTION["query"],
        chunks,
        chunk_vectors,
    )[:1]

    without_prompt = QUESTION["query"]
    rag_prompt = build_prompt(
        QUESTION["query"],
        search_results,
    )

    results = [
        run_tiny(without_prompt, rag_prompt),
        run_evo(without_prompt, rag_prompt),
        run_rlt(without_prompt, rag_prompt),
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        format_markdown(results, search_results),
        encoding="utf-8",
    )

    print(f"\n比較結果を保存しました: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
