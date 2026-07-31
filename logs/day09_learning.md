# Day 9 Learning Memo

## 今日のテーマ

PythonからOllamaのOpenAI互換APIを通してTinySwallowへ質問を送り、回答をターミナルへ表示する。

## 今日理解したこと

### PythonからローカルLLMを呼び出す流れ

今回の処理は、次の順番で進む。

1. Pythonスクリプトが標準入力から質問を受け取る。
2. Pythonが `localhost:11434/v1` にあるOllamaのOpenAI互換APIへ質問を送る。
3. Ollamaが指定されたTinySwallowを動かす。
4. TinySwallowの回答がOllamaからPythonへ返る。
5. Pythonが回答本文をターミナルへ表示する。

ユーザー自身の言葉では、「Pythonのスクリプトから `localhost:11434` に質問が送られて、それにTinySwallowが回答した」と理解した。

### 標準入力

`input()` を使うと、Pythonスクリプトの実行中にターミナルから文字列を受け取れる。

```python
question = input("質問を入力してください: ")
```

入力された質問は `question` 変数へ保存され、APIへ送るメッセージの内容として使われる。

### OpenAI互換Chat API

`client.chat.completions.create()` を使い、会話形式でTinySwallowへリクエストを送った。

`messages` には発言者の種類を表す `role` と、発言内容を表す `content` を設定する。今回はユーザーからの質問なので、`role` は `user` とした。

回答本文は次の場所から取り出した。

```python
response.choices[0].message.content
```

### 小型モデルの回答確認

TinySwallowはローカルLLMについて詳しい回答を生成できた。一方で、韓国語が混じった不自然な単語や、補足が必要な説明もあった。

モデルの回答はそのまま正しいと考えず、自然さや事実関係を人間が確認する必要がある。

## 今日出てきた重要用語

- 標準入力: プログラムがターミナルなどから受け取る入力
- OpenAI互換API: OpenAI APIと似た形式でモデルを利用できるAPI
- Chat Completions: `messages` を渡して会話形式の回答を生成する仕組み
- `role`: メッセージの発言者の種類
- `content`: メッセージの本文
- `localhost`: 自分のPCを指す接続先

## 実行したコマンドと、その意味

```bash
curl http://localhost:11434/v1/models
```

OllamaのOpenAI互換APIへ接続できることと、利用可能なモデル名を確認した。

```bash
touch src/ask_tinyswallow.py
```

Day9の成果物となる空のPythonファイルを作成した。

```bash
python src/ask_tinyswallow.py
```

作成したスクリプトを実行し、標準入力の受け取りとTinySwallowの回答表示を確認した。

## まだ曖昧なこと

- `response.choices[0]` のようなレスポンス構造の詳しい意味
- `system` や `assistant` を含む他の `role` の使い分け
- 複数回の会話履歴を保持する方法

これらはDay10以降で扱う。

## 自分の言葉でのまとめ

Pythonのスクリプトから `localhost:11434` のOllamaへ質問を送り、Ollamaを通してTinySwallowの回答を受け取れる。
