# Day 8 Learning Memo

## 今日のテーマ

Pythonの仮想環境を準備し、OllamaのOpenAI互換APIへPythonから接続する。

## 今日理解したこと

### Pythonの仮想環境

仮想環境は、プロジェクトごとにPythonパッケージを分離して管理する仕組み。

`.venv` を有効化すると、`python` や `pip` はMac全体の環境ではなく、`.venv` 内のものを使う。ターミナルのプロンプトに `(.venv)` と表示されることで、有効化されていることを確認できる。

### OllamaのOpenAI互換API

Ollamaは、OpenAIのAPIと互換性のある形式でローカルモデルを呼び出せる。

今回使用した接続先は `http://localhost:11434/v1`。

- `localhost`: 自分のPC
- `11434`: Ollamaが使用するポート
- `/v1`: OpenAI互換APIのベースパス

`OpenAI` クライアントを使っていても、`base_url` を `http://localhost:11434/v1` に設定することで、OpenAIのクラウドではなくローカルのOllamaへ接続できる。

### APIキーの扱い

`openai` パッケージでは `api_key` の指定が必要だが、ローカルのOllamaへ接続する今回の構成では、本物のOpenAI APIキーは使用しない。コードではプレースホルダーとして `api_key="ollama"` を指定した。

### 依存パッケージの記録

`pip freeze` は、仮想環境へインストールされているパッケージとバージョンを一覧にする。

今回直接導入したのは `openai==2.50.0` で、それ以外の多くは `openai` が必要とする依存パッケージ。これらを `requirements.txt` に保存することで、後から同じ環境を再現しやすくなる。

### Gitから仮想環境を除外する理由

`.venv` には多数の環境依存ファイルが入るため、通常はGitで管理しない。`.gitignore` に `.venv/` を追加し、仮想環境のディレクトリ全体を除外した。

## 今日出てきた重要用語

- 仮想環境: プロジェクトごとにPythonとパッケージの環境を分離する仕組み
- API: ソフトウェア同士が決められた形式でやり取りするための窓口
- OpenAI互換API: OpenAI APIと同様のリクエスト形式を利用できるAPI
- `base_url`: APIクライアントが接続する基準URL
- `localhost`: 自分のPCを表すホスト名
- ポート: 同じPC内で接続先のサービスを区別する番号
- 依存パッケージ: あるパッケージが動作するために必要な別のパッケージ

## 実行したコマンドと、その意味

```bash
which python3
python3 --version
```

使用されるPythonの場所とバージョンを確認した。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

リポジトリ専用の仮想環境を作成し、有効化した。

```bash
python -m pip install openai
python -c "import openai; print(openai.__version__)"
```

仮想環境へ `openai` パッケージを導入し、読み込みとバージョンを確認した。

```bash
curl http://localhost:11434/v1/models
```

OllamaのOpenAI互換APIへ直接アクセスし、モデル一覧がJSONで返ることを確認した。

```bash
python src/check_ollama_api.py
```

Pythonの `openai` パッケージからOllamaへ接続し、モデル一覧を取得した。

```bash
python -m pip freeze > requirements.txt
```

仮想環境内のパッケージとバージョンを `requirements.txt` に記録した。

```bash
git status --short
```

変更ファイルを短い形式で確認し、`.venv/` がGitの管理対象から除外されていることを確認した。

## まだ曖昧なこと

- `/v1/chat/completions` を使って、実際にモデルへ質問を送る方法
- `messages` 配列や `system`、`user`、`assistant` の役割
- APIで生成パラメータを指定する方法

これらはDay9以降のPythonからTinySwallowを呼び出す実装で確認する。

## 自分の言葉でのまとめ

Pythonコードの `base_url="http://localhost:11434/v1"` が、接続先をOpenAIのクラウドではなくローカルのOllamaへ切り替えている。

仮想環境を使えば、プロジェクトに必要なPythonパッケージを分離して管理できる。`requirements.txt` へバージョンを記録し、`.venv/` はGitから除外することで、リポジトリを扱いやすい状態にできる。
