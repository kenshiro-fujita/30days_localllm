from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

question = input("質問を入力してください: ")

response = client.chat.completions.create(
    model="hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M",
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
)

print(response.choices[0].message.content)