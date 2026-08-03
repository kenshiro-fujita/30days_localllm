import json
import math
import urllib.request
from pathlib import Path


# 分割対象となるMarkdownファイル
SOURCE_PATH = Path("notes/day14_api_summary.md")

# 比較するチャンクサイズ
CHUNK_SIZES = [300, 500, 1000]

# OllamaのEmbedding APIと、文章のベクトル化に使うモデル
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"


def split_by_size(text, chunk_size):
    """文章を指定した文字数ごとに分割する。"""

    # 先頭からchunk_size文字ずつ切り出し、リストとして返す
    return [
        text[start:start + chunk_size]
        for start in range(0, len(text), chunk_size)
    ]


def embed(texts):
    """文章をOllamaへ送り、Embeddingの一覧を取得する。"""

    # PythonのデータをJSONへ変換し、APIへ送れるバイト列にする
    data = json.dumps({
        "model": EMBED_MODEL,
        "input": texts,
    }).encode("utf-8")

    # OllamaのEmbedding APIへ送るHTTPリクエストを組み立てる
    request = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    # APIの結果から、文章ごとのベクトルを取り出す
    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    return result["embeddings"]


def cosine_similarity(vector_a, vector_b):
    """2つのベクトルの向きがどれくらい近いか計算する。"""

    # 同じ位置にある数値同士を掛け、すべて足して内積を求める
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    # それぞれのベクトルの大きさを求める
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


# Markdownファイルを文字列として読み込む
text = SOURCE_PATH.read_text(encoding="utf-8")

# 同じ質問を各チャンクサイズで検索するため、1度だけ入力する
query = input("検索したい内容を入力してください: ").strip()
query_vector = embed([query])[0]

print(f"ファイル: {SOURCE_PATH}")
print(f"文字数: {len(text)}")
print(f"質問: {query}")

# 各サイズの1位を最後に並べて比較する
comparison = []

# 同じ文書を異なるチャンクサイズで分割し、分割数を比較する
for chunk_size in CHUNK_SIZES:
    chunks = split_by_size(text, chunk_size)

    print("\n" + "=" * 60)
    print(f"{chunk_size}文字チャンク（全{len(chunks)}件）")
    print("=" * 60)

    # チャンクをまとめてEmbeddingし、質問との類似度を求める
    chunk_vectors = embed(chunks)
    search_results = []

    for index, (chunk, chunk_vector) in enumerate(
        zip(chunks, chunk_vectors),
        start=1,
    ):
        score = cosine_similarity(query_vector, chunk_vector)
        search_results.append((score, index, chunk))

    # スコアの高い順に上佉3件を表示する
    search_results.sort(reverse=True)
    best_score, best_index, _ = search_results[0]
    comparison.append(
        (chunk_size, len(chunks), best_score, best_index)
    )

    for rank, (score, index, chunk) in enumerate(
        search_results[:3],
        start=1,
    ):
        # 改行を空白に変換し、検索で取得した内容を読みやすく表示する
        normalized_chunk = " ".join(chunk.split())
        preview = normalized_chunk[:240]
        suffix = " ..." if len(normalized_chunk) > 240 else ""

        print(f"\n{rank}位 | チャンク{index} | スコア {score:.4f}")
        print("-" * 60)
        print(f"{preview}{suffix}")


print("\n" + "=" * 60)
print("1位の結果をサイズごとに比較")
print("=" * 60)

for chunk_size, chunk_count, score, index in comparison:
    print(
        f"{chunk_size:>4}文字 | 全{chunk_count:>2}件 | "
        f"チャンク{index:>2} | スコア {score:.4f}"
    )
