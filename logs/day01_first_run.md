# Day 1 Log

## やったこと

- PC環境、Python、Git、Ollama の有無を確認した。
- Day 1 用の基本ディレクトリを作成した。
- 汎用評価質問10問を `eval/questions.md` に固定した。
- 評価用の架空素材を `eval/materials.md` に固定した。
- Ollama を Homebrew でインストールし、サービス起動した。
- TinySwallow Q5_K_M を取得し、Ollamaで初回推論した。
- 評価質問から Q1/Q2/Q5 の3問を TinySwallow に投げ、回答ログを残した。
- Day 1仕上げとして、評価質問・評価素材・ログが揃っていることを確認した。
- Ollama APIでTinySwallowが現在も利用可能なことを確認した。

## 環境確認

- OS: macOS 26.5.2
- CPU architecture: arm64
- Python: 3.9.6
- Git: 2.50.1
- Homebrew: 5.1.6
- Ollama: 0.31.1
- Ollama service: 起動済み
- TinySwallow: `hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M`
- TinySwallow size: 1.1 GB
- TinySwallow family: qwen2
- TinySwallow parameter size: 1.54B
- TinySwallow context length: 32768
- Git repository: 初期化済み

## 分かったこと

- Apple Silicon Mac なので、計画上は Mac / Apple Silicon ルートで進める。
- Python と Git はすでに利用できる。
- Ollama は Homebrew で導入できた。
- TinySwallow はOllama経由で取得・推論できた。
- TinySwallow は `http://localhost:11434/api/tags` からも確認できた。
- Day 1 の評価セットは、後日のモデル比較、RAG評価、最終評価で再利用する重要な固定資産になる。
- TinySwallowの回答は自然な日本語で返るが、初回観察では一部に不正確または怪しい説明が混ざる。
- Day 1時点では、10問すべての評価実行は不要。Day 5で同一質問セットを使って回収する。

## 詰まったこと

- 最初は `ollama --version` が `command not found` になったが、Homebrewでインストールして解消した。
- メモリ確認の `sysctl hw.memsize` は実行環境の制限で取得できなかった。
- 通常権限の `curl` では `localhost:11434` に接続できず、承認付き実行でOllama API疎通を確認した。
- 通常権限の `git init` は `.git: Operation not permitted` で失敗したが、承認付き実行で初期化できた。

## 初回推論

### CLIスモークテスト

Command:

```bash
ollama run hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M "ローカルLLMとは何ですか。30字以内で説明してください。"
```

Output:

```text
ローカルのコンピュータ上に構築された大規模言語モデルです。
ユーザーが直接使用可能、インターネット依存度低い。
```

### Q1. ローカルLLMの説明

Prompt:

```text
ローカルLLMとは何ですか。クラウド型LLMとの違いを、非エンジニアにも分かるように説明してください。
```

Output:

```text
ローカルLLMは「Local」とある通り、自分自身のコンピュータやスマートフォンなどのデバイスにインストールして使う大規模言語モデルのことです。

一方でクラウド型LLMは、GoogleやAmazonのような企業が運営するサーバーなどからアクセスするサービスを利用することを指します。

それぞれの違いを非エンジニアにも分かりやすく説明すると、

ローカルLLM:
- プログラミングスキルがあれば自分自身でインストールできます。
- データ通信量が少なく、インターネット接続さえあれば利用できます。
- サーバーの問題やセキュリティに気を配る必要はありません。

クラウド型LLM:
- 特別な知識は不要で簡単に使うことができます。
- いつでもどこからでもアクセス可能なので、場所を選ばずに使えるのが特徴です。
- サーバーの維持管理が面倒ですが、その分サービス料金はローカルに比べて安い場合が多いです。

どちらもメリットとデメリットがあるので、自分の状況やニーズに合わせて選択することが重要となります。
```

Observation:

- 概要はそれらしい。
- 「ローカルLLMはインターネット接続さえあれば利用できる」「サーバーの問題やセキュリティに気を配る必要はない」は不正確。
- Day 5では「自然さ」と「正確さ」を分けて評価する必要がある。

### Q2. RAGの説明

Prompt:

```text
RAGとは何ですか。なぜLLMに外部資料を渡す必要があるのか、具体例を使って説明してください。
```

Output:

```text
RAGは Retrieval-Augmented Generation の略で、日本語では「検索付き生成」と訳されることがあります。

これはAI言語モデルが自分自身の知識に加えて、外部の文書やデータから情報を引き出す技術です。従来のAI（大規模言語モデル）は与えられたテキストの内容だけを参考にして回答を作成しますが、RAGではそのテキスト情報だけでなく、インターネット上の様々なソースからの知識も活用することでより広範で豊富な情報を提供することができます。

LLMに外部資料を渡す必要性:
1. 情報の正確さ
2. 範囲と多様性
3. クリエイティビティ

具体例:
- 事実確認と情報収集
- クリエイティブな文書作成
- 複雑な問題解決
```

Observation:

- RAGの略称と大枠は合っている。
- LLMを `Long-Text Model` と説明しており誤り。
- RAGを「インターネット上の様々なソース」と限定気味に説明しているが、社内文書や固定ナレッジも対象になる。

### Q5. 社内LLM利用のリスク整理

Prompt:

```text
社内でLLMを使うときのリスクを、情報漏えい、誤回答、運用負荷の3観点で整理してください。
```

Output:

```text
社内でLLMを使用する際は、情報漏えい、誤回答、運用負荷の3つの観点からリスクを洗い出し、対策を講じることが重要です。

情報漏えいリスク:
- LLMは大量のデータを処理し、その過程で機密情報が含まれる可能性がある。
- 個人情報を含むデータはLLM訓練に使用しない。

誤回答リスク:
- LLMの学習に偏りがある場合、特定の観点では不適切な答えが生成される可能性がある。
- LLMが生成した回答に対して人間による確認・修正体制を構築する。

運用負荷リスク:
- 複雑なLLMの運用には計算能力、メンテナンス費用などが必要。
- 運用監視ツールによる定期的な確認・異常検知体制を構築する。
```

Observation:

- 3観点に分ける指示には従えている。
- 対策はやや一般論で、社内利用時の入力制御、ログ管理、権限管理、回答レビューなどは追加で見たい。

## 明日やること

- Day 2 のトークン分割メモ `notes/day02_tokens.md` に進む。
- 余力があれば、初回コミットを行う。

## Day 1仕上げ確認

- `eval/questions.md`: 作成済み。Q1〜Q10の評価質問を固定済み。
- `eval/materials.md`: 作成済み。架空素材A〜Dを固定済み。
- `logs/day01_first_run.md`: 作成済み。このファイルをDay 1の日次ログとして扱う。
- Ollama API: `http://localhost:11434/api/tags` でTinySwallowを確認済み。
- Git状態: リポジトリ初期化済み。初回コミットは未実施。

## Day 1完了判定

- TinySwallowが起動した: 完了
- `eval/questions.md` を作った: 完了
- `eval/materials.md` を作った: 完了
- 2〜3問だけでも回答ログを残した: 完了
- よって、Day 1は完了扱いとする。

## 成果物

- `eval/questions.md`
- `eval/materials.md`
- `logs/day01_first_run.md`
- TinySwallowのローカル推論確認
- Ollama APIでのモデル確認
