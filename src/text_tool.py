import json

from openai import OpenAI, OpenAIError

MODEL = "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def call_llm(messages, response_format=None):
    request_options = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0,
    }

    if response_format is not None:
        request_options["response_format"] = response_format

    response = client.chat.completions.create(**request_options)
    return response.choices[0].message.content


print("モードを選んでください")
print("1: 要約")
print("2: 文章改善")
print("3: 分類")

mode = input("> ")

if mode == "1":
    system_prompt = (
        "あなたは日本語文章の要約アシスタントです。"
        "入力された文章の重要な内容を残し、簡潔に要約してください。"
    )
elif mode == "2":
    system_prompt = (
        "あなたは日本語文章の校正者です。"
        "語尾、助詞、句読点、不自然な表現だけを直してください。"
        "元の文章に含まれる情報を削除してはいけません。"
        "元の文章にない情報を追加してはいけません。"
        "入力から確認できない内容を推測してはいけません。"
        "改善後の文章だけを出力してください。"
    )
elif mode == "3":
    system_prompt = (
        "あなたは日本語文章の分類アシスタントです。"
        "入力された文章を「質問」「依頼」「感想」「その他」の"
        "いずれか1つに分類し、分類名だけを出力してください。"
    )
else:
    print("1、2、3のいずれかを入力してください。")
    raise SystemExit

print("処理する文章を入力してください")
text = input("> ")

if not text.strip():
    print("文章が入力されていません。")
    raise SystemExit

try:
    result = call_llm(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            *(
                [
                    {
                        "role": "user",
                        "content": (
                            "このツールは文章を入れたら誤字を直したり、"
                            "敬語にしたりできるので使いやすいと思った。"
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": (
                            "このツールは、文章を入力すると誤字の修正や"
                            "敬語への変更ができるため、使いやすいと思いました。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "このモデルは小さくてパソコンで動くし、"
                            "日本語の質問にも答えられるのが良いと思う。"
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": (
                            "このモデルは小型でパソコン上で動作し、"
                            "日本語の質問にも回答できる点が良いと思います。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "この機能は結果がすぐ見れて便利だけど、"
                            "設定する項目が多くて少し分かりにくいと思った。"
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": (
                            "この機能は、結果をすぐに確認できて便利ですが、"
                            "設定項目が多く、少し分かりにくいと思いました。"
                        ),
                    },
                ]
                if mode == "2"
                else []
            ),
            {
                "role": "user",
                "content": text,
            },
        ]
        )
    final_result = result

    if mode == "2":
        validation_raw = call_llm(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "あなたは文章校正結果の検証者です。"
                        "原文と校正結果を比較し、情報の追加・削除・意味変更を"
                        "それぞれ分けて検出してください。"
                        "問題が1つでもあればvalidをfalseにしてください。"
                        "JSONオブジェクトだけを出力してください。"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "原文:\n"
                        "この道具は軽くて赤いので持ち運びやすいと思った。\n\n"
                        "校正結果:\n"
                        "この道具は軽量で価格も安く、持ち運びに便利です。"
                    ),
                },
                {
                    "role": "assistant",
                    "content": (
                        '{"valid":false,'
                        '"added":["価格が安い"],'
                        '"removed":["赤い"],'
                        '"changed":["持ち運びやすいと思ったが、便利だという断定に変わった"]}'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"原文:\n{text}\n\n"
                        f"校正結果:\n{result}\n\n"
                        "同じJSON形式で検証してください。"
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        validation = json.loads(validation_raw)

        added = validation["added"]
        removed = validation["removed"]
        changed = validation["changed"]

        has_issues = bool(added or removed or changed)
        is_valid = not has_issues
        if not is_valid:
            final_result = text

        print("\n検証結果:")
        print(f"LLMの判定: {validation['valid']}")
        print(f"Pythonの判定: {is_valid}")
        print(f"追加: {added}")
        print(f"削除: {removed}")
        print(f"意味変更: {changed}")

    print("\n結果:")
    print(final_result)

except OpenAIError as error:
    print("TinySwallowの呼び出しに失敗しました。")
    print(f"エラー: {error}")

except json.JSONDecodeError as error:
    print("検証結果のJSON解析に失敗しました。")
    print(f"エラー: {error}")

except KeyError as error:
    print(f"検証結果に必要な項目がありません: {error}")