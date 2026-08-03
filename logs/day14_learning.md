# Day 14 学習メモ

## 今日のテーマ

Week 2で作ったPythonスクリプトを振り返り、APIクライアント、接続先のOllama、実際に文章を生成するTinySwallowの関係を整理する。

## 今日理解したこと

### `OpenAI`はAPIへ接続するためのクライアント

```python
from openai import OpenAI
```

ここで読み込む`OpenAI`は、OpenAI互換APIそのものでも、OpenAIのLLMでもない。OpenAI公式のPythonライブラリが提供する、APIへリクエストを送るためのクライアントである。

クライアントは、HTTPリクエストを組み立てて接続先へ送り、返ってきたレスポンスをPythonから扱いやすくする道具である。

### Pythonクライアントの接続先をOllamaへ変更する

```python
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
```

`OpenAI`クライアントは通常OpenAIのサービスへの接続に使われるが、`base_url`で接続先を変更できる。今回は`localhost`を指定しているため、リクエストは自分のPCで起動しているOllamaへ送られる。Ollamaが起動していなければ接続できない。

### OpenAI互換APIはアプリ向けの呼び出し形式

APIは、プログラム同士が決められた方法で情報を受け渡すための窓口である。接続先のURL、送る項目、返ってくるデータの形などに決まりがある。

OpenAIは、`model`や`messages`を送って回答を受け取るAPI形式を提供している。Ollamaもその呼び出し方の一部へ対応しているため、OpenAI公式のPythonクライアントからOllamaを呼び出せる。このように、OpenAIと似た決まりで呼び出せることを「OpenAI互換」と呼ぶ。

Ollamaがリクエストを受け取り、TinySwallowが処理できる入力へ変換する。OpenAIのサーバーやモデルを使っているわけではない。

OpenAIのモデルを使うという意味ではなく、OpenAI風の注文票を使って、ローカルのOllamaへ注文するイメージで理解した。

### アプリ、Ollama、モデルには別々の役割がある

- Pythonアプリ: ユーザー入力、`messages`、会話履歴、出力検証を管理する
- Ollama: APIの窓口となり、ローカルLLMを管理・実行する
- TinySwallow: 渡された入力をもとに文章を生成する
- `openai`ライブラリ: OpenAI形式のAPIリクエストを作成・送信する

### 会話履歴はPython側で保持する

TinySwallowが過去の会話を自動的に記憶するわけではない。Python側でuserとassistantの発言を`messages`へ追加し、APIを呼ぶたびに履歴をまとめてモデルへ渡す。

### 出力はPython側でも検証する

LLMへJSON形式を指示するだけでは、正しい出力は保証されない。次の項目をPython側でも確認する。

1. JSONなどの要求した形式として解析できるか
2. 必要な項目が存在するか
3. 値が許可範囲内か
4. 情報の追加・削除・意味変更がないか

問題があれば、エラー表示、再生成、原文へのフォールバックなどで安全側へ処理する。

## 今日出てきた重要用語

- APIクライアント: APIへリクエストを送り、レスポンスを受け取るためのプログラム側の道具
- API: プログラム同士が決められた方法で情報を受け渡すための窓口
- OpenAI互換API: OpenAIのAPIと似た項目やデータ形式で呼び出せるAPI
- `base_url`: APIクライアントの接続先を指定する値
- `localhost`: プログラムを実行している自分のPCを表すホスト名
- ポート番号: 同じPC上で動く複数のサービスを区別する番号。Ollamaの標準は`11434`
- `messages`: system、user、assistantのメッセージを並べた会話データ
- ストリーミング: 完成した回答を待たず、生成された断片から順次受け取る方式
- 構造化出力: JSONなど、プログラムから扱いやすい決まった構造の出力
- フォールバック: 本来の出力を採用できない場合に使う代替処理

## 実行したコマンドと、その意味

```bash
ls -1 src
```

Week 2で作ったPythonスクリプトを一覧表示した。

```bash
sed -n '1,220p' src/check_ollama_api.py
sed -n '1,220p' src/ask_tinyswallow.py
sed -n '1,260p' src/chat_cli.py
sed -n '1,280p' src/stream_chat.py
sed -n '1,300p' src/json_classifier.py
```

各スクリプトのコードを表示し、API接続、文章生成、会話履歴、ストリーミング、JSON出力の仕組みを振り返った。

```bash
grep -nE '^(MODEL|PROMPTS|def |if __name__)' src/text_tool.py
```

`text_tool.py`のモデル定数や関数など、コードの構造を抽出しようとした。チャット表示で`__name__`が太字記法へ変換され、意図した条件の一部は使えなかった。

```bash
sed -n '1,260p' notes/day14_api_summary.md
sed -n '1,320p' README.md
git diff --check
```

作成したまとめとREADMEを表示し、保存内容と変更後の形式を確認した。`git diff --check`は何も表示されず、形式上の問題は検出されなかった。

## まだ曖昧なこと

- OpenAI互換APIでOllamaが対応している機能の範囲
- 会話履歴が長くなった場合の具体的な管理方法
- LLMによる検証の誤検出を減らす方法
- 不合格になった回答を再生成する方法

## 自分の言葉でのまとめ

`from openai import OpenAI`で読み込むのは、APIへリクエストを送るためのPythonクライアントであり、APIやモデルそのものではない。`base_url`を`localhost`へ変更することで、そのクライアントから自分のPCのOllamaへ接続する。OllamaはOpenAIと似た形式のリクエストを受け付け、TinySwallowを実行する。Pythonが入力・履歴・検証を管理し、OllamaがAPIの窓口とモデル実行を担当し、TinySwallowが文章を生成する。
