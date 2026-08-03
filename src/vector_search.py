import json
import math
import urllib.request


# OllamaのEmbedding APIと、文章のベクトル化に使うモデル
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"


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

    # APIを呼び出し、返ってきたJSONをPythonのデータへ変換する
    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    # APIの結果から、文章ごとのベクトルだけを取り出す
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

    # 内積をベクトルの大きさで割り、向きの近さを求める
    return dot_product / (magnitude_a * magnitude_b)


# 類似検索の対象として、あらかじめ保存しておく文章
documents = [
    "猫がソファの上で昼寝をしています。",
    "犬が公園で元気に走っています。",
    "動物園には珍しい動物がたくさんいます。",
    "キャベツを使った濃い味の炒め物を作ります。",
    "忙しい日は短時間で作れる料理が便利です。",
    "休日に時間をかけてカレーを煮込みます。",
    "パソコンを使ってPythonを勉強しています。",
    "スマートフォンは多くの人が持つ身近な端末です。",
    "電車に乗って職場へ向かいます。",
    "雨の日は家で本を読んで過ごします。",
]


# 検索対象の10文章をまとめてベクトル化する
document_vectors = embed(documents)

# ユーザーから検索文を受け取り、前後の余分な空白を取り除く
query = input("検索したい内容を入力してください: ").strip()

# 入力された検索文を、文書と同じEmbeddingモデルでベクトル化する
query_vector = embed([query])[0]


# 各文章と質問文のコサイン類似度を計算する
search_results = []

for document, document_vector in zip(documents, document_vectors):
    score = cosine_similarity(query_vector, document_vector)
    search_results.append((score, document))


# 類似度が高い文章から順番に並べ替える
search_results.sort(reverse=True)


# 質問文と、スコア付きの検索結果を表示する
print(f"質問: {query}")
print("\n検索結果:")

for rank, (score, document) in enumerate(search_results, start=1):
    print(f"{rank}. {score:.4f}  {document}")