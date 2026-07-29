# ローカルLLM作成30日チャレンジ Day8(7月28日) PythonからOllamaのAPIへ接続する

ローカルLLM作成30日チャレンジのDay8です。

Week 1では、Ollamaでモデルを動かしながら、トークン、量子化、Transformerなどの基礎を学びました。Day8からは、Pythonを使った実装へ進みます。

今回はPythonの仮想環境を作り、OllamaのOpenAI互換APIへ接続しました。

## 今日やったこと

### Pythonの仮想環境を作る

まず、現在使っているPythonを確認しました。

```bash
which python3
python3 --version
```

今回はHomebrewで導入したPython 3.14.6が使われていました。リポジトリには仮想環境がまだなかったため、次のコマンドで `.venv` を作りました。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

仮想環境は、プロジェクトごとにPythonパッケージを分けて管理するための仕組みです。有効化すると、ターミナルの先頭に `(.venv)` と表示されました。

続いて、OpenAI互換APIをPythonから扱うために `openai` パッケージを導入しました。

```bash
python -m pip install openai
```

今回は `openai 2.50.0` が入りました。`pip` を直接実行せず、`python -m pip` とすることで、現在有効な仮想環境のPythonへ導入していることを明確にしました。

### curlでOllamaのAPIを確認

Pythonコードを書く前に、OllamaのAPI自体が動いているかを確認しました。

```bash
curl http://localhost:11434/v1/models
```

このURLは、自分のPCを表す `localhost`、Ollamaの標準ポートである `11434`、OpenAI互換APIのベースパス `/v1` で構成されています。

実行すると、TinySwallowとQwenのモデル情報がJSONで返りました。これで、OllamaのOpenAI互換APIへ接続できることを確認できました。

### Pythonからモデル一覧を取得

次に、`src/check_ollama_api.py` を自分で作成しました。

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

models = client.models.list()

print("Ollamaへの接続に成功しました。")
for model in models.data:
    print(f"- {model.id}")
```

重要なのは、`base_url` にOllamaのURLを設定しているところです。`OpenAI` クライアントを使っていますが、接続先はOpenAIのクラウドではなく、自分のPCで動いているOllamaです。

`api_key="ollama"` も指定していますが、これは本物のOpenAI APIキーではありません。今回使ったライブラリでは何らかの値を設定する必要があるため、仮の値として `ollama` を入れています。

スクリプトを実行すると、Ollamaへの接続成功メッセージと、登録されている2つのモデルが表示されました。

```bash
python src/check_ollama_api.py
```

`curl` ではHTTP API自体の動作を確認し、Pythonでは `openai` パッケージから同じAPIを利用できることを確認しました。

### 後から再現できるように記録

環境を後から作り直せるよう、インストールしたパッケージとバージョンを `requirements.txt` に保存しました。

```bash
python -m pip freeze > requirements.txt
```

直接インストールしたのは `openai` ですが、`requirements.txt` には、その動作に必要な依存パッケージも記録されています。

また、仮想環境の中身をGitへ登録しないよう、`.gitignore` に次の設定を追加しました。

```gitignore
.venv/
```

最後に、仮想環境の作成、APIの確認、Pythonスクリプトの実行手順をREADMEへ追記しました。

## 今日のハマりポイント

今日は大きなエラーもなく、スムーズに進められました。

途中で確認したところ、`.gitignore` に `.venv/` が入っていませんでした。そのままでは仮想環境内の大量のファイルをGitへ登録する可能性があるため、除外設定を追加しました。

また、`OpenAI` という名前のクライアントを使うため、最初はOpenAIのクラウドへ接続しているようにも見えます。実際には `base_url="http://localhost:11434/v1"` と設定したことで、ローカルのOllamaへ接続しています。

## 今日の感想

これまではOllamaのコマンドからモデルを動かしていましたが、今回はPythonからOllamaへ接続できました。まだモデルへ質問を送ったわけではありませんが、ローカルLLMをプログラムから利用する入口までは作れたと思います。

特に、接続先を決めているのが `base_url` だと自分の言葉で確認できたのは大きかったです。

次は、このOpenAI互換APIを使ってPythonからTinySwallowへ実際に質問を送ります。
