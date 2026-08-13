# ローカルLLM作成30日チャレンジ

ローカルLLMの基礎から、API利用、RAG、ファインチューニング、評価までを30日間で学ぶリポジトリです。

## ローカルでLLMを動かすとは

ローカルでLLMを動かすとは、クラウド上のAIサービスだけに頼らず、自分のPCにLLMをセットアップし、推論や文章生成に活用することです。

既存の学習済みモデルをOllamaなどへ導入して使うことも含みます。モデルを一から学習させることだけを意味するわけではありません。

### メリット

- モデルの取得後は、インターネット接続がなくても利用できる
- 入力内容を外部のAIサービスへ送信せず、手元の環境内で処理できる
- 使用するモデルや設定を自分で管理できる

ただし、ローカルで動かすだけで無条件に安全になるわけではありません。利用ツールの通信設定、ログの保存場所、PC自体のセキュリティは別途確認する必要があります。

### デメリット

- PCのメモリや処理性能によって、動かせるモデルが制限される
- 大規模なクラウドLLMと比べて、回答精度や知識量で劣る場合がある
- モデルの導入、更新、設定を自分で管理する必要がある

## Week 1で学んだこと

### トークン

LLMが文章を読み取り、生成するときに扱う情報の単位です。文字や単語と完全に一致するとは限りません。

### temperature

次トークン候補の確率分布を調整し、回答のランダムさや多様性に影響する設定です。

### 量子化

モデルのパラメータを低い精度で表現し、容量、メモリ使用量、計算負荷を減らす技術です。その代わり、出力品質が低下する可能性があります。

### Attention

入力中のトークン同士の関連性を計算し、次の予測でどのトークンをどれくらい重視するか決める仕組みです。

### Transformer

Attentionなどの処理を何層も組み合わせ、文脈を踏まえて次のトークンを予測するモデル構造です。

### 指示チューニング

「指示と望ましい回答」の組を使って追加学習し、人間の依頼に応じやすく調整することです。

## モデル比較で分かったこと

TinySwallowとQwenを同じ質問で比較し、同じくらいのサイズのモデルでも、回答には得意不得意があると分かりました。

モデルはサイズだけで判断せず、実際の用途に近い質問で比較することが重要です。

## Python環境とOllama APIの疎通確認

### 仮想環境の準備

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install openai
```

仮想環境を有効化すると、ターミナルのプロンプトに `(.venv)` と表示されます。

### OllamaのAPIを確認

Ollamaが起動している状態で、次を実行します。

```bash
curl http://localhost:11434/v1/models
```

APIは、プログラム同士が決められた方法で情報を受け渡すための窓口です。`http://localhost:11434/v1`は、自分のPCで動くOllamaがAPIリクエストを受け付ける接続先です。

Pythonコードでは、OpenAI公式の`openai`ライブラリをAPIクライアントとして使います。これはOpenAIのモデルを読み込むという意味ではありません。`base_url`を上記のOllamaのアドレスへ変更することで、リクエストはOpenAIではなくローカルのOllamaへ送られます。

Ollamaは、OpenAIのAPIと似た項目やデータ形式でリクエストを受け付けられます。この性質を「OpenAI互換」と呼びます。

### Pythonから疎通確認

```bash
python src/check_ollama_api.py
```

接続に成功すると、Ollamaに登録されているモデル一覧が表示されます。

## Week 2で作ったPythonスクリプト

実行前にOllamaを起動し、Pythonの仮想環境を有効にします。

### TinySwallowへ1回質問する

```bash
python src/ask_tinyswallow.py
```

質問を1回入力し、TinySwallowが生成した回答を一括表示します。

### 会話履歴を持つCLI

```bash
python src/chat_cli.py
```

Python側の`messages`へuserとassistantの発言を追加し、会話のたびに履歴全体をモデルへ渡します。`exit`を入力すると終了します。

### ストリーミング応答

```bash
python src/stream_chat.py
```

回答を断片ごとに受け取り、生成途中から画面へ表示します。接続エラー、APIエラー、`Ctrl+C`による中断も処理します。

### JSON形式の文章分類

```bash
python src/json_classifier.py
```

入力した文章を分類・要約・感情分析し、JSON形式で受け取ります。Python側でJSONの構文、必要な項目、値の許可範囲を確認します。

## 日本語文章ツール

TinySwallowを使い、日本語文章を要約・改善・分類するCLIアプリです。

Ollamaが起動し、TinySwallowが利用できる状態で次を実行します。

```bash
python src/text_tool.py
```

起動後、処理モードを選択します。

```text
1: 要約
2: 文章改善
3: 分類
```

モード番号を入力してEnterを押した後、処理する文章を入力します。

### 実行例

```text
モードを選んでください
1: 要約
2: 文章改善
3: 分類
> 3
処理する文章を入力してください
> 明日の会議資料を確認してください。

結果:
依頼
```

小型LLMの出力は必ずしも指示どおりになるとは限りません。文章改善では、入力にない情報の追加や、元の情報の削除が起きる場合があります。

文章改善モードではFew-shotの例を与え、生成後に別のLLM呼び出しで情報の追加・削除・意味変更を検証します。最終的な合否はPython側で決定し、不合格の場合は改善結果を採用せず原文を表示します。

## Week 2のまとめ

Pythonアプリ、Ollama、TinySwallow、OpenAI互換APIの関係や、各スクリプトの役割は[`notes/day14_api_summary.md`](notes/day14_api_summary.md)にまとめています。

## RAGで外部資料を使う

Week 3では、Markdown文書をチャンクへ分割し、`bge-m3`でEmbeddingを作成して、質問に近いチャンクをLLMへ渡す最小RAGを実装しました。

```bash
python rag/rag_qa.py
```

RAGはモデル自体へ知識を学習させる方法ではありません。検索した外部資料を回答時の文脈として渡すため、更新される情報や回答根拠を確認したい用途に向いています。

## 自作データでQwenをファインチューニングする

Week 4では、会議メモを「要点・決定事項・次の行動」へ整理する`messages`形式のJSONLを作り、MLX LoRAでQwenを追加学習しました。

- 学習データ：`dataset/train.jsonl`
- 検証データ：`dataset/valid.jsonl`
- 固定評価：`eval/ft_questions.md`
- adapter：`finetune/tuned_adapter_v1/`
- 学習結果：`finetune/smoke_test_result.md`、`eval/day27_ft_eval.md`

adapterはMLX-LMでbase modelへ統合し、llama.cppでGGUFへ変換しました。さらにOllama登録時に`q4_K_M`へ量子化し、次のコマンドで呼び出せます。

```bash
ollama run tuned-qwen-day29
```

Ollama上のモデルサイズは約4.7GBです。配備手順とスモークテスト結果は[`finetune/day29_deployment.md`](finetune/day29_deployment.md)にまとめています。

配備に使った約14GBの統合済みモデルと約15GBのF16 GGUFは、Ollama登録後に中間生成物として削除しています。再変換する場合はbase model、LoRA adapter、配備記録から再生成できます。

## 最終評価で分かったこと

TinySwallow、base Qwen、tuned Qwenを固定問題で比較した結果、tuned Qwenはbase Qwenの単純な上位互換にはなりませんでした。

- 入力情報を保持し、base Qwenより大きな捏造が減ったケースがあった
- RAG説明や業務ヒアリングなど、回答の方向性が良くなったケースがあった
- 学習させた「要点・決定事項・次の行動」の形式を守れないケースが増えた
- 学習データ由来とみられる表現が、関係の薄い汎用質問にも現れた
- Train lossが下がっても、形式遵守や実用上の品質が一様に改善するとは限らなかった

FTはモデル全体を単純に強くする操作ではなく、特定の振る舞いを変える操作として捉える必要があります。実際の用途に近い固定問題で、狙った改善と副作用の両方を評価することが重要です。

全モデルの出力は質問単位で[`eval/runs/day29_final_outputs.md`](eval/runs/day29_final_outputs.md)へ統合し、結論と代表ケースは[`eval/final_eval.md`](eval/final_eval.md)へまとめています。
