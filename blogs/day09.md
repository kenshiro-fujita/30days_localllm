# ローカルLLM作成30日チャレンジ Day9(7月29日) PythonからTinySwallowに質問する

ローカルLLM作成30日チャレンジのDay9です。

前回はPythonからOllamaのOpenAI互換APIへ接続し、利用できるモデルの一覧を取得しました。今回はそこから一歩進めて、ターミナルに入力した質問をTinySwallowへ送り、回答を表示するスクリプトを作りました。

## 今日やったこと

### Ollamaとモデルを確認

最初に、OllamaのOpenAI互換APIへ接続できるか確認しました。

```bash
curl http://localhost:11434/v1/models
```

実行すると、QwenとTinySwallowの情報がJSONで返りました。これでOllamaが起動していることと、今回使うTinySwallowのモデル名を確認できました。

### ターミナルから質問を受け取る

Day9の成果物として、`src/ask_tinyswallow.py` を自分で作成しました。

まずは、Pythonの `input()` を使ってターミナルから質問を受け取るところだけを書きました。

```python
question = input("質問を入力してください: ")
print(f"受け取った質問: {question}")
```

スクリプトを実行して「今日の天気は？」と入力すると、同じ質問が表示されました。これで、入力した文字列が `question` 変数へ保存されていることを確認できました。

### TinySwallowへ質問を送る

次に、Day8で使った接続設定へChat APIの呼び出しを追加しました。

```python
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
```

`messages` の `role` は発言者の種類、`content` は発言内容です。今回はターミナルから入力した質問をユーザーの発言として送るため、`role` に `user`、`content` に `question` を設定しました。

返ってきたデータのうち、`response.choices[0].message.content` が回答本文です。最後にこれを `print()` して、ターミナルへ表示しています。

### 実際に質問してみる

スクリプトを実行し、「ローカルLLMとはなんですか？」と質問しました。

```bash
python src/ask_tinyswallow.py
```

TinySwallowは、クラウドサービスを必要とせず手元の機器で動かせることや、プライバシー、ハードウェア要件などについて回答しました。

今回の流れを自分なりに整理すると、Pythonのスクリプトから `localhost:11434` のOllamaへ質問が送られ、指定したTinySwallowが回答し、その内容がPythonへ返ってくるという理解です。

## 今日のハマりポイント

今日はエラーもなく、PythonからTinySwallowの回答を表示するところまで進められました。

ただし、生成された回答には `컴퓨ンテーション` という韓国語混じりの不自然な単語がありました。また、ローカルLLMの利用者が自分でモデルを訓練するようにも読める説明がありましたが、実際には既存モデルを取得して推論だけ行う使い方もあります。

小型のローカルLLMでも詳しい文章は生成できますが、自然な文章だからといって、すべて正確とは限りません。回答の言葉遣いや事実関係は人間が確認する必要があると改めて分かりました。

## 今日の感想

Day8ではAPIからモデル一覧を取得しただけでしたが、今回は自分で入力した質問にTinySwallowが答えるところまでつながりました。

Python、Ollama、TinySwallowの関係も、「PythonからOllamaへ送り、Ollamaがモデルを動かす」という流れで少し具体的に見えてきたと思います。

次は `messages` の役割を整理し、会話履歴を持つCLIを作ります。
