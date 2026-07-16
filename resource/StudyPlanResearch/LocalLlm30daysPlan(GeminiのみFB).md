# ローカルLLM入門30日チャレンジ 最終版
作成日: 2026-07-14  
開始日: 2026-07-14(火)  
期間: 30日間  
学習時間: 平日1時間、土日祝3時間  

---

## 1. このチャレンジの目的

この30日チャレンジの目的は、ローカルLLMをゼロから事前学習することではない。

目的は、以下を一通り体験し、LLMの動作原理と実装感を理解すること。

- ローカルLLMを自分のPCで動かす
- Sakana AIのTinySwallowを中心に、日本語LLMの挙動を観察する
- PythonからローカルLLMをAPIとして呼び出す
- EmbeddingとRAGの基本を理解する
- Qwen2.5-1.5B-InstructでLoRA/QLoRAファインチューニングを一周する
- TinySwallow、base Qwen、tuned Qwenを比較評価する
- 「RAGでできること」と「ファインチューニングでできること」の違いを説明できるようになる

---

## 2. 最終ゴール

30日後のゴールは以下。

> Sakana AIのTinySwallowを中心にローカルLLMの推論・API利用・RAGを理解し、Qwen2.5-1.5B-InstructでLoRA/QLoRAファインチューニングを一周し、TinySwallow・base Qwen・tuned Qwenの違いを自分の言葉で説明できる状態になる。

---

## 3. モデルの役割分担

| 用途 | モデル | 役割 |
|---|---|---|
| ローカル推論 | SakanaAI/TinySwallow-1.5B-Instruct-GGUF | このチャレンジの主役。Ollamaまたはllama.cppで動かす |
| Python API利用 | SakanaAI/TinySwallow-1.5B-Instruct-GGUF | ローカルLLMをアプリから呼び出す対象 |
| RAG | SakanaAI/TinySwallow-1.5B-Instruct-GGUF | 検索結果を渡して回答させる対象 |
| FT練習 | Qwen/Qwen2.5-1.5B-Instruct | LoRA/QLoRAファインチューニングの練習用 |
| TinySwallowのFT | 余力課題 | 30日チャレンジの必須成果物にはしない |

### なぜこの分担にするか

TinySwallowはSakana AIの日本語向け小型モデルであり、このチャレンジのモチベーションに合っている。一方で、初心者がいきなりTinySwallowをファインチューニング対象にすると、ライブラリ・トークナイザー・特殊トークン・変換周りで詰まる可能性がある。

そのため、推論・API利用・RAGはTinySwallowを使い倒す。  
ファインチューニングは情報量が多く、学習環境の事例が豊富なQwen2.5-1.5B-Instructに固定する。

Qwen2.5-1.5B-InstructはTinySwallowの学生モデルとして使われた系譜に近いため、単なる妥協ではなく、TinySwallow理解にもつながるルートである。

---

## 4. 基本方針

### やること

- OllamaでTinySwallowを動かす
- 日本語LLMの出力を観察する
- PythonからOllama APIを叩く
- CLIツールを作る
- Embeddingとベクトル検索を試す
- 最小RAGを作る
- Qwen2.5-1.5B-InstructでLoRA/QLoRAを試す
- シンセティックデータを作ってFTする
- モデル比較評価を行う
- READMEに全成果をまとめる

### やらないこと

- ゼロから基盤モデルを事前学習する
- 本格的なGraphRAGを作る
- 社内展開や権限管理まで作る
- LangGraph風のエージェント実装まで広げる
- TinySwallowのFTを必須ゴールにする
- 機密情報や個人情報を学習データに入れる

---

## 5. 環境ルート

### 第一候補: Mac / Apple Siliconの場合

- 推論: Ollama
- FT候補: mlx-lm
- 代替: Google Colab + Unsloth

### Windows + NVIDIA GPUの場合

- 推論: Ollama
- FT候補: Unsloth / Transformers + PEFT
- 代替: Google Colab + Unsloth

### GPUなし、または環境構築で詰まる場合

- 推論: ローカルOllama
- FT: Google Colab + Unsloth
- 方針: ローカルにこだわりすぎず、30日完走を優先する

---

## 6. 主要コマンド例

### TinySwallowをOllamaで起動する例

```bash
ollama run hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M
```

### llama.cpp serverで起動する例

```bash
brew install llama.cpp
llama serve -hf SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M
```

### Python仮想環境の例

```bash
mkdir local-llm-30days
cd local-llm-30days

python -m venv .venv
source .venv/bin/activate

pip install requests numpy
```

---

## 7. 推奨ディレクトリ構成

```text
local-llm-30days/
  README.md
  PLAN.md
  notes/
    day02_tokens.md
    day04_quantization.md
    day06_transformer.md
    day14_api_summary.md
    day15_embedding.md
    day17_rag_architecture.md
    day21_rag_vs_finetune.md
    day22_finetune_strategy.md
  logs/
    day01_first_run.md
    day03_generation_params.md
  src/
    ask_tinyswallow.py
    chat_cli.py
    stream_chat.py
    json_classifier.py
    text_tool.py
    vector_search.py
    chunk_text.py
    validate_jsonl.py
  rag/
    rag_qa.py
    docs/
    index/
  dataset/
    dataset_spec.md
    generate_prompt.md
    raw_generated_v0.jsonl
    train.jsonl
    valid.jsonl
    eval.jsonl
  finetune/
    smoke_test_result.md
    adapter_smoke/
    tuned_adapter_v1/
  eval/
    day05_model_compare.md
    day20_rag_eval.md
    day27_ft_eval.md
    day28_tinyswallow_vs_tuned_qwen.md
    final_eval.md
  next_challenge.md
```

---

## 8. 毎日のログ形式

各Dayの最後に必ず以下を書く。

```md
# Day X Log

## やったこと
-

## 分かったこと
-

## 詰まったこと
-

## 明日やること
-

## 成果物
-
```

---

## 9. 詰まった時のルール

- 平日に詰まったら15分で切り上げる
- 原因究明を続けず、詰まった内容をログに残す
- 重い作業は土日祝に回す
- ローカルFTで詰まったらColab + Unslothに逃げる
- TinySwallowのFTで詰まったら、Qwen2.5-1.5B-Instructで完走を優先する
- 完璧なモデル作成より、LLMの仕組み理解と一周体験を優先する

---

## 10. Codexへの基本指示

Codexには以下の方針で日々サポートさせる。

```md
あなたはローカルLLM入門30日チャレンジの学習支援エージェントです。

目的は、ユーザーが30日間でローカルLLMの推論、API利用、RAG、LoRA/QLoRAファインチューニング、評価を一周できるよう支援することです。

ユーザーは過去に約3年弱のエンジニア経験がありますが、現在は非エンジニアです。説明は初心者に寄せつつ、実装は省略しすぎないでください。

毎日のタスクでは以下を守ってください。

- その日の学習テーマから外れすぎない
- 平日は1時間で終わる粒度に分解する
- エラーが出たら原因候補を3つ以内に絞る
- 15分以上詰まりそうなら、回避策を提案する
- コードは動く最小構成を優先する
- READMEやログに残すべき内容も提案する
- 社外秘、個人情報、会社の機密情報をデータセットに入れないよう注意する
```

---

# 11. 日別計画

## Day 0

| 項目 | 内容 |
|---|---|
| Day | Day 0 |
| 日付 | 7/13 |
| 曜日 | 月 |
| 学習テーマ | 環境ルート決定 |
| 具体的な学習手順 | 1. PCのチップとメモリを確認する。<br>2. Apple Silicon Macなら第一候補をMLXにする。<br>3. ローカルFTが重そうならGoogle Colab + Unslothをバックアップにする。<br>4. Ollama、Python、Git、VS Code/Codexの利用準備をする。<br>5. `local-llm-30days` リポジトリを作成する。 |
| 習得スキル | 環境選定、学習ルート判断、開発環境準備 |
| 備考 | すでに7/13を過ぎている場合は、Day 1開始前に30分だけ実施する。 |

---

## Day 1

| 項目 | 内容 |
|---|---|
| Day | Day 1 |
| 日付 | 7/14 |
| 曜日 | 火 |
| 学習テーマ | TinySwallowをローカルで動かす |
| 具体的な学習手順 | 1. Ollamaを起動する。<br>2. `SakanaAI/TinySwallow-1.5B-Instruct-GGUF` をOllamaで実行する。<br>3. 日本語で10個質問する。<br>4. 回答速度、回答品質、違和感をメモする。 |
| 習得スキル | ローカルLLM実行、Ollama基本操作、GGUFモデル利用 |
| 備考 | 平日1h。成果物：`logs/day01_first_run.md` |

---

## Day 2

| 項目 | 内容 |
|---|---|
| Day | Day 2 |
| 日付 | 7/15 |
| 曜日 | 水 |
| 学習テーマ | トークンの仕組み |
| 具体的な学習手順 | 1. 日本語と英語の短文を複数入力する。<br>2. 回答の安定性や長さを比較する。<br>3. トークンが文字単位ではないことを整理する。<br>4. 日本語LLMでトークン効率が重要な理由を書く。 |
| 習得スキル | トークン、語彙、入力長、コンテキスト長 |
| 備考 | 平日1h。成果物：`notes/day02_tokens.md` |

---

## Day 3

| 項目 | 内容 |
|---|---|
| Day | Day 3 |
| 日付 | 7/16 |
| 曜日 | 木 |
| 学習テーマ | 生成パラメータ |
| 具体的な学習手順 | 1. 同じ質問をtemperature低め/高めで試す。<br>2. top_pの意味を調べる。<br>3. 事実回答、アイデア出し、文章生成で違いを見る。<br>4. 結果を表にする。 |
| 習得スキル | temperature、top_p、確率的生成、再現性 |
| 備考 | 平日1h。成果物：`logs/day03_generation_params.md` |

---

## Day 4

| 項目 | 内容 |
|---|---|
| Day | Day 4 |
| 日付 | 7/17 |
| 曜日 | 金 |
| 学習テーマ | 量子化の理解 |
| 具体的な学習手順 | 1. GGUF、Q4、Q5、Q8、F16を調べる。<br>2. TinySwallowの量子化版を確認する。<br>3. Q5_K_Mを使う理由を整理する。<br>4. 軽量化で何が犠牲になるかを書く。 |
| 習得スキル | 量子化、モデルサイズ、推論速度、品質劣化 |
| 備考 | 平日1h。成果物：`notes/day04_quantization.md` |

---

## Day 5

| 項目 | 内容 |
|---|---|
| Day | Day 5 |
| 日付 | 7/18 |
| 曜日 | 土 |
| 学習テーマ | モデル比較 |
| 具体的な学習手順 | 1. TinySwallowに評価用質問を10個投げる。<br>2. 可能ならQwen2.5-1.5B-Instructや別の日本語対応モデルも比較する。<br>3. 自然さ、正確さ、指示追従性を評価する。<br>4. 「TinySwallowの得意・不得意」をまとめる。 |
| 習得スキル | モデル比較、評価観点作成、日本語LLM観察 |
| 備考 | 休日3h。成果物：`eval/day05_model_compare.md` |

---

## Day 6

| 項目 | 内容 |
|---|---|
| Day | Day 6 |
| 日付 | 7/19 |
| 曜日 | 日 |
| 学習テーマ | Transformerと次トークン予測 |
| 具体的な学習手順 | 1. LLMは次トークン予測モデルであることを理解する。<br>2. Attention、Transformer、事前学習、指示チューニングを調べる。<br>3. TinySwallowがInstruction-tunedモデルである意味を整理する。<br>4. 図解メモを作る。 |
| 習得スキル | Transformer、Attention、事前学習、Instruction tuning |
| 備考 | 休日3h。成果物：`notes/day06_transformer.md` |

---

## Day 7

| 項目 | 内容 |
|---|---|
| Day | Day 7 |
| 日付 | 7/20 |
| 曜日 | 月 |
| 学習テーマ | Week 1整理 |
| 具体的な学習手順 | 1. Day1〜6のメモを読み返す。<br>2. 用語集を作る。<br>3. 「ローカルでLLMを動かすとは何か」を文章化する。<br>4. README初版を書く。 |
| 習得スキル | 技術用語の言語化、README作成、学習整理 |
| 備考 | 祝日3h。成果物：`README.md` 初版 |

---

## Day 8

| 項目 | 内容 |
|---|---|
| Day | Day 8 |
| 日付 | 7/21 |
| 曜日 | 火 |
| 学習テーマ | Python環境構築 |
| 具体的な学習手順 | 1. Python仮想環境を作る。<br>2. `requests` またはOpenAI互換クライアントを入れる。<br>3. `src/`, `logs/`, `notes/` を作る。<br>4. 実行手順をREADMEに書く。 |
| 習得スキル | Pythonプロジェクト構成、仮想環境、依存管理 |
| 備考 | 平日1h。成果物：リポジトリ初期構成 |

---

## Day 9

| 項目 | 内容 |
|---|---|
| Day | Day 9 |
| 日付 | 7/22 |
| 曜日 | 水 |
| 学習テーマ | PythonからTinySwallowを呼ぶ |
| 具体的な学習手順 | 1. Ollamaを起動する。<br>2. PythonからOllama APIへリクエストを送る。<br>3. 標準入力から質問を受け取る。<br>4. 応答をターミナルに表示する。 |
| 習得スキル | API呼び出し、HTTP、ローカルLLMのプログラム利用 |
| 備考 | 平日1h。成果物：`src/ask_tinyswallow.py` |

---

## Day 10

| 項目 | 内容 |
|---|---|
| Day | Day 10 |
| 日付 | 7/23 |
| 曜日 | 木 |
| 学習テーマ | 会話履歴 |
| 具体的な学習手順 | 1. `messages` 配列を作る。<br>2. user/assistant/system roleを整理する。<br>3. 会話履歴を持つCLIを作る。<br>4. 履歴が長い時の挙動を観察する。 |
| 習得スキル | Chat形式API、role、会話履歴、コンテキスト管理 |
| 備考 | 平日1h。成果物：`src/chat_cli.py` |

---

## Day 11

| 項目 | 内容 |
|---|---|
| Day | Day 11 |
| 日付 | 7/24 |
| 曜日 | 金 |
| 学習テーマ | ストリーミング応答 |
| 具体的な学習手順 | 1. Ollama APIのstream出力を使う。<br>2. 応答を逐次表示する。<br>3. 一括表示と体感速度を比較する。<br>4. エラー処理を入れる。 |
| 習得スキル | ストリーミング、CLI UX、例外処理 |
| 備考 | 平日1h。成果物：`src/stream_chat.py` |

---

## Day 12

| 項目 | 内容 |
|---|---|
| Day | Day 12 |
| 日付 | 7/25 |
| 曜日 | 土 |
| 学習テーマ | 構造化出力 |
| 具体的な学習手順 | 1. TinySwallowにJSON形式で返すよう指示する。<br>2. 文章分類、要約、感情分類を試す。<br>3. JSON parse失敗ケースを観察する。<br>4. system promptで出力安定化を試す。 |
| 習得スキル | JSON出力、プロンプト設計、構造化レスポンス |
| 備考 | 休日3h。成果物：`src/json_classifier.py` |

---

## Day 13

| 項目 | 内容 |
|---|---|
| Day | Day 13 |
| 日付 | 7/26 |
| 曜日 | 日 |
| 学習テーマ | ミニアプリ作成 |
| 具体的な学習手順 | 1. 日本語文章を入力するCLIを作る。<br>2. 要約、改善、分類の3モードを作る。<br>3. TinySwallowを裏側で呼ぶ。<br>4. READMEに実行例を追記する。 |
| 習得スキル | ローカルLLMアプリ化、CLI設計、プロンプト分岐 |
| 備考 | 休日3h。成果物：`src/text_tool.py` |

---

## Day 14

| 項目 | 内容 |
|---|---|
| Day | Day 14 |
| 日付 | 7/27 |
| 曜日 | 月 |
| 学習テーマ | Week 2整理 |
| 具体的な学習手順 | 1. PythonからLLMを使う流れを図解する。<br>2. Ollama、モデル、API、Pythonアプリの関係を書く。<br>3. 作ったスクリプトを整理する。<br>4. READMEに使い方を書く。 |
| 習得スキル | API利用の全体像理解、ドキュメント化 |
| 備考 | 平日1h。成果物：`notes/day14_api_summary.md` |

---

## Day 15

| 項目 | 内容 |
|---|---|
| Day | Day 15 |
| 日付 | 7/28 |
| 曜日 | 火 |
| 学習テーマ | Embedding基礎 |
| 具体的な学習手順 | 1. Embeddingとは文章をベクトルにすることだと理解する。<br>2. 類似文章が近いベクトルになることを調べる。<br>3. 日本語文章を5〜10個用意する。<br>4. 類似度検索の用途をメモする。 |
| 習得スキル | Embedding、ベクトル、類似度検索 |
| 備考 | 平日1h。成果物：`notes/day15_embedding.md` |

---

## Day 16

| 項目 | 内容 |
|---|---|
| Day | Day 16 |
| 日付 | 7/29 |
| 曜日 | 水 |
| 学習テーマ | ベクトル検索実装 |
| 具体的な学習手順 | 1. 日本語Embeddingモデルまたは軽量Embeddingを使う。<br>2. 10個程度の文章をベクトル化する。<br>3. 質問文に近い文章を検索する。<br>4. スコア付きで検索結果を表示する。 |
| 習得スキル | ベクトル検索、コサイン類似度、検索スコア |
| 備考 | 平日1h。成果物：`src/vector_search.py` |

---

## Day 17

| 項目 | 内容 |
|---|---|
| Day | Day 17 |
| 日付 | 7/30 |
| 曜日 | 木 |
| 学習テーマ | RAG全体像 |
| 具体的な学習手順 | 1. RAGを「検索→文脈注入→回答生成」に分けて理解する。<br>2. RAGとFTの違いを軽く整理する。<br>3. TinySwallowに検索結果を渡す設計を考える。<br>4. RAG構成図を書く。 |
| 習得スキル | RAG、外部知識、コンテキスト注入 |
| 備考 | 平日1h。成果物：`notes/day17_rag_architecture.md` |

---

## Day 18

| 項目 | 内容 |
|---|---|
| Day | Day 18 |
| 日付 | 7/31 |
| 曜日 | 金 |
| 学習テーマ | チャンク分割 |
| 具体的な学習手順 | 1. Markdownメモを用意する。<br>2. 300字、500字、1000字で分割する。<br>3. 検索しやすさの違いを見る。<br>4. チャンクサイズと検索精度の関係を書く。 |
| 習得スキル | チャンク設計、検索単位、コンテキスト設計 |
| 備考 | 平日1h。成果物：`src/chunk_text.py` |

---

## Day 19

| 項目 | 内容 |
|---|---|
| Day | Day 19 |
| 日付 | 8/1 |
| 曜日 | 土 |
| 学習テーマ | 最小RAG実装 |
| 具体的な学習手順 | 1. Markdown文書をチャンク化する。<br>2. Embeddingして保存する。<br>3. 質問に近いチャンクを検索する。<br>4. 検索結果をTinySwallowに渡して回答させる。 |
| 習得スキル | RAG実装、検索結果のプロンプト注入、根拠付き回答 |
| 備考 | 休日3h。成果物：`rag/rag_qa.py` |

---

## Day 20

| 項目 | 内容 |
|---|---|
| Day | Day 20 |
| 日付 | 8/2 |
| 曜日 | 日 |
| 学習テーマ | RAG評価 |
| 具体的な学習手順 | 1. テスト質問を10個作る。<br>2. RAGなし回答とRAGあり回答を比較する。<br>3. 根拠に沿っているか確認する。<br>4. 間違い方を分類する。 |
| 習得スキル | RAG評価、根拠性、ハルシネーション観察 |
| 備考 | 休日3h。成果物：`eval/day20_rag_eval.md` |

---

## Day 21

| 項目 | 内容 |
|---|---|
| Day | Day 21 |
| 日付 | 8/3 |
| 曜日 | 月 |
| 学習テーマ | RAGとFTの使い分け |
| 具体的な学習手順 | 1. RAGは知識を外から渡す方法だと整理する。<br>2. FTは振る舞いや形式を寄せる方法だと整理する。<br>3. 向いている用途を表にする。<br>4. FTで学習させたい振る舞いを決める。 |
| 習得スキル | RAG/FTの使い分け、学習対象の設計 |
| 備考 | 平日1h。成果物：`notes/day21_rag_vs_finetune.md` |

---

## Day 22

| 項目 | 内容 |
|---|---|
| Day | Day 22 |
| 日付 | 8/4 |
| 曜日 | 火 |
| 学習テーマ | FT基礎とモデル固定 |
| 具体的な学習手順 | 1. SFT、LoRA、QLoRA、adapter、mergeを調べる。<br>2. FT対象を `Qwen/Qwen2.5-1.5B-Instruct` に固定する。<br>3. TinySwallowは推論・RAG用、QwenはFT練習用と役割分担を書く。<br>4. Mac/MLXルートとColab/UnslothルートをREADMEに記載する。 |
| 習得スキル | SFT、LoRA、QLoRA、adapter、モデル選定 |
| 備考 | 平日1h。成果物：`notes/day22_finetune_strategy.md` |

---

## Day 23

| 項目 | 内容 |
|---|---|
| Day | Day 23 |
| 日付 | 8/5 |
| 曜日 | 水 |
| 学習テーマ | FTデータセット設計 |
| 具体的な学習手順 | 1. 学習させたい振る舞いを1つ決める。<br>2. 例：文章を丁寧に改善する、要約する、業務メモ化する。<br>3. instruction/input/output形式を決める。<br>4. 商用LLMにデータ生成させるためのプロンプトを作る。 |
| 習得スキル | instruction dataset設計、JSONL設計、データ生成プロンプト設計 |
| 備考 | 平日1h。成果物：`dataset/dataset_spec.md`, `dataset/generate_prompt.md` |

---

## Day 24

| 項目 | 内容 |
|---|---|
| Day | Day 24 |
| 日付 | 8/6 |
| 曜日 | 木 |
| 学習テーマ | シンセティックデータ生成① |
| 具体的な学習手順 | 1. ChatGPT/Claude/Gemini等で30〜50件のJSONL候補を生成する。<br>2. 生成プロンプトを調整する。<br>3. 明らかに低品質な例を除外する。<br>4. 5件を評価用に分離する。 |
| 習得スキル | シンセティックデータ生成、品質確認、評価用データ分離 |
| 備考 | 平日1h。成果物：`dataset/raw_generated_v0.jsonl`, `dataset/eval_seed.jsonl` |

---

## Day 25

| 項目 | 内容 |
|---|---|
| Day | Day 25 |
| 日付 | 8/7 |
| 曜日 | 金 |
| 学習テーマ | シンセティックデータ生成② |
| 具体的な学習手順 | 1. データを100件前後まで増やす。<br>2. 重複、表記ゆれ、長すぎる出力を修正する。<br>3. train/valid/evalに分ける。<br>4. JSONLとして読み込めるか検証スクリプトを作る。 |
| 習得スキル | データクリーニング、train/valid/eval分割、JSONL検証 |
| 備考 | 平日1h。成果物：`dataset/train.jsonl`, `dataset/valid.jsonl`, `dataset/eval.jsonl`, `src/validate_jsonl.py` |

---

## Day 26

| 項目 | 内容 |
|---|---|
| Day | Day 26 |
| 日付 | 8/8 |
| 曜日 | 土 |
| 学習テーマ | FT環境構築＋簡易学習 |
| 具体的な学習手順 | 1. 第一候補としてMLX、詰まる場合はColab + Unslothを使う。<br>2. Qwen2.5-1.5B-InstructでLoRAチュートリアルを実行する。<br>3. Day25の自作データで1エポックまたは少ないstepだけ回す。<br>4. loss、adapter生成、推論確認まで行う。<br>5. エラーが出た場合はこの日に原因を出し切る。 |
| 習得スキル | LoRA環境構築、学習実行、adapter生成、初回デバッグ |
| 備考 | 休日3h。成果物：`finetune/smoke_test_result.md`, `finetune/adapter_smoke/` |

---

## Day 27

| 項目 | 内容 |
|---|---|
| Day | Day 27 |
| 日付 | 8/9 |
| 曜日 | 日 |
| 学習テーマ | 本番FT＋評価 |
| 具体的な学習手順 | 1. Day26で通った設定を使う。<br>2. 学習step、epoch、learning rateを決めて本番学習する。<br>3. base Qwenとtuned Qwenに同じ評価質問を投げる。<br>4. 良くなった点、悪くなった点、壊れた点を記録する。 |
| 習得スキル | 本番LoRA/QLoRA、評価比較、ハイパーパラメータ観察 |
| 備考 | 休日3h。成果物：`finetune/tuned_adapter_v1/`, `eval/day27_ft_eval.md` |

---

## Day 28

| 項目 | 内容 |
|---|---|
| Day | Day 28 |
| 日付 | 8/10 |
| 曜日 | 月 |
| 学習テーマ | TinySwallowとの比較 |
| 具体的な学習手順 | 1. TinySwallow、base Qwen、tuned Qwenに同じ質問を投げる。<br>2. TinySwallowの自然さと、tuned Qwenのタスク特化を比較する。<br>3. 「FTで変わるもの・変わらないもの」を整理する。<br>4. TinySwallowにFTを適用する場合の次課題を書く。 |
| 習得スキル | モデル横断比較、FT効果の理解、次課題設計 |
| 備考 | 平日1h。成果物：`eval/day28_tinyswallow_vs_tuned_qwen.md` |

---

## Day 29

| 項目 | 内容 |
|---|---|
| Day | Day 29 |
| 日付 | 8/11 |
| 曜日 | 火 |
| 学習テーマ | 配備と最終評価 |
| 具体的な学習手順 | 1. 可能ならadapter mergeまたはGGUF変換を試す。<br>2. Ollamaまたはllama.cppで使う流れを調べる。<br>3. 20問の評価セットでTinySwallow、base Qwen、tuned Qwenを比較する。<br>4. ローカルLLMとして使える状態をREADMEにまとめる。 |
| 習得スキル | モデル配備、GGUF/Ollama理解、最終評価 |
| 備考 | 祝日3h。成果物：`eval/final_eval.md` |

---

## Day 30

| 項目 | 内容 |
|---|---|
| Day | Day 30 |
| 日付 | 8/12 |
| 曜日 | 水 |
| 学習テーマ | 総まとめ |
| 具体的な学習手順 | 1. 30日間の成果物を整理する。<br>2. READMEを完成させる。<br>3. 「LLMの動作原理」「RAG」「FT」「評価」を自分の言葉でまとめる。<br>4. 次の30日チャレンジ案を書く。 |
| 習得スキル | 技術理解の言語化、成果物整理、次アクション設計 |
| 備考 | 平日1h。成果物：完成版README、`next_challenge.md` |

---

# 12. 評価用質問セットの例

## TinySwallow観察用

```md
1. ローカルLLMとは何か、初心者向けに説明してください。
2. RAGとファインチューニングの違いを説明してください。
3. 以下の文章を3行で要約してください。
4. 以下の文章をビジネス向けに丁寧に書き換えてください。
5. 日本語LLMを使うメリットを説明してください。
6. temperatureを上げると何が変わりますか。
7. この文章をJSON形式で分類してください。
8. 架空の社内メモを読み、ToDoを抽出してください。
9. 与えられた根拠だけを使って回答してください。
10. 分からない場合は分からないと答えてください。
```

## FT評価用

```md
1. 雑なメモを丁寧な業務文に直してください。
2. 長い文章を3点に要約してください。
3. 箇条書きメモから議事録風に整えてください。
4. 曖昧な依頼文を明確なタスクに分解してください。
5. カジュアルすぎる文章を社内向けに整えてください。
6. 入力文から目的、背景、次アクションを抽出してください。
7. 文章のトーンを変えずに短くしてください。
8. 情報不足の点を質問として列挙してください。
9. 作業ログを日報風に変換してください。
10. README向けの説明文に書き換えてください。
```

---

# 13. FT用データセットの基本スキーマ

JSONLの1行は以下の形式を基本とする。

```json
{"instruction":"次の文章を丁寧な業務文に書き換えてください。","input":"これ今日中にやっといて。無理なら早めに言って。","output":"本日中にご対応いただけますでしょうか。難しい場合は、早めにご共有いただけますと助かります。"}
```

またはChat形式。

```json
{"messages":[{"role":"system","content":"あなたは日本語の業務文を整えるアシスタントです。"},{"role":"user","content":"次の文章を丁寧な業務文に書き換えてください。\nこれ今日中にやっといて。無理なら早めに言って。"},{"role":"assistant","content":"本日中にご対応いただけますでしょうか。難しい場合は、早めにご共有いただけますと助かります。"}]}
```

実際に使う形式は、Day 26で選ぶFTライブラリに合わせる。

---

# 14. シンセティックデータ生成プロンプト例

```md
あなたは日本語の業務文データセットを作るアシスタントです。

目的:
小型LLMをLoRAファインチューニングし、雑な日本語メモを丁寧で分かりやすい業務文に変換できるようにしたいです。

以下のJSONL形式で、30件のデータを作成してください。

条件:
- 1行に1 JSON object
- instruction, input, output の3キーを使う
- outputは自然な日本語にする
- inputにはカジュアル、曖昧、短すぎるメモを入れる
- outputでは丁寧だが堅すぎないビジネス文にする
- 個人情報、会社名、実在人物名は入れない
- 内容は一般的な架空の業務にする
- Markdownのコードブロックは不要
- JSONとしてパースできる形にする

例:
{"instruction":"次の文章を丁寧な業務文に書き換えてください。","input":"これ今日中にやっといて。無理なら早めに言って。","output":"本日中にご対応いただけますでしょうか。難しい場合は、早めにご共有いただけますと助かります。"}
```

---

# 15. 30日後に説明できるべきこと

このチャレンジ完了時点で、以下を説明できる状態を目指す。

| 観点 | 説明できるべきこと |
|---|---|
| ローカルLLM | クラウドAPIではなく、自分のPC上でLLMを動かす意味 |
| TinySwallow | Sakana AIの日本語向け小型LLMとしての位置づけ |
| Qwen2.5 | FT練習用モデルとして使う理由 |
| トークン | LLMが文字ではなくトークン単位で扱うこと |
| 生成パラメータ | temperatureやtop_pで出力が変わる理由 |
| 量子化 | モデルを軽くして動かす仕組みとトレードオフ |
| GGUF | ローカル推論で使われるモデル形式 |
| API | PythonからLLMを部品として呼び出す方法 |
| Embedding | 文章をベクトル化して検索する意味 |
| RAG | 検索した外部知識をLLMに渡す仕組み |
| FT | モデルの振る舞いを学習で寄せる方法 |
| LoRA | 全重みを更新せず、追加のadapterを学習する考え方 |
| QLoRA | 量子化モデルを使って省メモリでFTする考え方 |
| 評価 | baseモデルとtunedモデルを比較する方法 |

---

# 16. 参考情報

- TinySwallow-1.5B-Instruct-GGUF: `SakanaAI/TinySwallow-1.5B-Instruct-GGUF`
- FT練習モデル: `Qwen/Qwen2.5-1.5B-Instruct`
- 推論ランタイム: Ollama / llama.cpp
- Mac向けFT候補: mlx-lm
- Colab向けFT候補: Unsloth
- 重要なバックアップ方針: ローカルFTで詰まったらColab + Unslothに逃げる

---

# 17. 次の30日チャレンジ候補

今回の30日が終わった後は、以下のどれかに進むとよい。

## 候補1: ローカルAIエージェント30日チャレンジ

- ツール呼び出し
- ファイル操作
- TODO管理
- RAG連携
- 権限管理
- 監査ログ

## 候補2: RAG実践30日チャレンジ

- チャンク設計
- Embedding比較
- Vector DB比較
- rerank
- 評価セット作成
- 回答根拠の可視化

## 候補3: 日本語小型LLM改善30日チャレンジ

- TinySwallowのFT検証
- 日本語データセット作成
- GGUF変換
- Ollama登録
- 評価ベンチ作成
- 実用CLI化
