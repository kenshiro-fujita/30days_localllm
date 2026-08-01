import json

from openai import OpenAI

MODEL = "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
text = input("分類する文章を入力してください: ")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "あなたは日本語文章の分析器です。\n"
                "入力された文章を分析し、次の3項目を出力してください。\n"
                "- categoryは必ず次の4つから1つだけ選ぶこと\n"
                "  質問: 回答を尋ねる文章\n"
                "  依頼: 相手に行動を求める文章\n"
                "  感想: 感じたことや評価を述べる文章\n"
                "  その他: 上記に当てはまらない文章\n"
                "  複数のラベルを結合してはいけません\n"
                "- summary: 入力内容の短い要約\n"
                "- sentiment: 肯定的・否定的・中立のいずれか\n"
                "JSONオブジェクトを1つだけ出力してください。\n"
                "JSONの前後に説明を書かず、Markdownも使わないでください。\n"
                '出力例: {"category":"感想","summary":"アプリが使いやすい",'
                '"sentiment":"肯定的"}'
                ),
        },
        {
            "role": "user",
            "content": text,
        },
    ],
    temperature=0,
    response_format={"type": "json_object"},
)

raw_output = response.choices[0].message.content
print("LLMの生出力:")
print(raw_output)

try:
    result = json.loads(raw_output)

    category = result["category"]
    summary = result["summary"]
    sentiment = result["sentiment"]

    allowed_categories = {"質問", "依頼", "感想", "その他"}
    allowed_sentiments = {"肯定的", "否定的", "中立"}

    if category not in allowed_categories:
        print(f"想定外の分類です: {category}")
    elif sentiment not in allowed_sentiments:
        print(f"想定外の感情分類です: {sentiment}")
    else:
        print("解析結果:")
        print(f"分類: {category}")
        print(f"要約: {summary}")
        print(f"感情: {sentiment}")

except json.JSONDecodeError as error:
    print("JSONの解析に失敗しました。")
    print(f"エラー: {error}")

except KeyError as error:
    print(f"必要な項目がありません: {error}")