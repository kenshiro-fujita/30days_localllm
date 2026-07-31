from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

messages = [
    {
        "role": "system",
        "content": "日本語で簡潔に回答してください。過去の会話内容について質問された場合は、messagesの会話履歴を参照して直接回答してください。",
    }
]

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    response = client.chat.completions.create(
        model="hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M",
        messages=messages,
    )

    assistant_reply = response.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply,
        }
    )

    print(f"TinySwallow: {assistant_reply}")