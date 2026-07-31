from openai import APIConnectionError, APIError, OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

try:
    question = input("質問を入力してください: ")

    stream = client.chat.completions.create(
        model="hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content is not None:
            print(content, end="", flush=True)

    print()

except APIConnectionError:
    print("Ollamaに接続できませんでした。Ollamaが起動しているか確認してください。")

except APIError as error:
    print(f"APIの処理中にエラーが発生しました: {error}")

except KeyboardInterrupt:
    print("\n処理を中断しました。")