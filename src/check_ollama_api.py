from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

models = client.models.list()

print("Ollamaへの接続に成功しました。")
for model in models.data:
    print(f"- {model.id}")