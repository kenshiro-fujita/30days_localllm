# ローカルLLM入門30日チャレンジ 最終確定完全版

作成日: 2026-07-14
開始日: 2026-07-14(火)
期間: 30日間
学習時間: 平日1時間、土日祝3時間
対象読者: Codex / AI学習支援エージェント / 未来の自分

---

# 0. この文書の位置づけ

この文書は、ローカルLLM入門30日チャレンジを進めるための完全コンテキストである。

Codexは、この文書を前提にして、毎日の学習・実装・ログ整理を支援すること。

このチャレンジでは、完璧なAIアプリや本番品質のモデルを作ることを目的にしない。
目的は、ローカルLLM、API利用、Embedding、RAG、LoRA/QLoRAファインチューニング、評価の一連の流れを、自分の手で小さく一周することである。

---

# 1. ユーザーの前提

ユーザーは現在、非エンジニアとして業務をしている。
ただし、過去にレガシー企業で約3年弱のエンジニア経験がある。

高度な機械学習や情報工学の専門家ではないが、業務システム開発経験はあり、Python、CLI、API、Gitなどに触れる基礎体力はある。

学習時間は以下。

```text
平日: 1時間
土日祝: 3時間
```

平日1時間で環境構築やエラー調査に深く入りすぎると崩れやすいため、詰まったら早めにログ化して休日に回す。

また、ユーザーは社内でAIX、つまりAI活用推進・業務変革支援に関わる立場を目指している。
そのため、このチャレンジは単なる趣味のLLM学習ではなく、将来的には以下に活かす想定である。

* 非エンジニア部門のAI活用支援
* 業務ヒアリングからAI活用候補を見つける
* AI機能のPoC設計
* RAGやAIエージェントの実現可能性判断
* エンジニアとの橋渡し
* AI機能の評価、安全性、運用観点の整理

---

# 2. このチャレンジの目的

この30日チャレンジの目的は、ローカルLLMをゼロから事前学習することではない。

目的は以下である。

```text
Sakana AIのTinySwallowを中心にローカルLLMを実際に動かしながら、
LLMの仕組み、API利用、Embedding、RAG、
LoRA/QLoRAファインチューニング、評価の流れを一通り理解する。
```

このチャレンジで身につけたいことは以下。

```text
ローカルLLMを動かせる
PythonからLLMを呼べる
OpenAI互換APIの意味が分かる
Embeddingとベクトル検索を説明できる
RAGの基本を説明できる
LoRA/QLoRAファインチューニングを一周できる
TinySwallow、base Qwen、tuned Qwenの違いを比較できる
RAGとFTの使い分けを説明できる
評価質問セットを使ってモデル比較できる
```

---

# 3. 最終ゴール

30日後のゴールは以下。

> Sakana AIのTinySwallowを中心にローカルLLMの推論・API利用・RAGを理解し、Qwen2.5-1.5B-InstructでLoRA/QLoRAファインチューニングを一周し、TinySwallow・base Qwen・tuned Qwenの違いを自分の言葉で説明できる状態になる。

---

# 4. モデルの役割分担

| 用途             | モデル                                       | 役割                       |
| -------------- | ----------------------------------------- | ------------------------ |
| ローカル推論         | `SakanaAI/TinySwallow-1.5B-Instruct-GGUF` | このチャレンジの主役。Ollamaで動かす    |
| Python API利用   | `SakanaAI/TinySwallow-1.5B-Instruct-GGUF` | OpenAI互換API経由で呼び出す対象     |
| RAG            | `SakanaAI/TinySwallow-1.5B-Instruct-GGUF` | 検索結果を渡して回答させる対象          |
| Embedding      | `bge-m3`                                  | 日本語文書のベクトル化に使う           |
| FT練習           | `Qwen/Qwen2.5-1.5B-Instruct`              | LoRA/QLoRAファインチューニングの練習用 |
| TinySwallowのFT | `SakanaAI/TinySwallow-1.5B-Instruct`      | 余力課題。必須成果物にはしない          |

---

# 5. なぜこの分担にするか

TinySwallowはSakana AIの日本語向け小型モデルであり、このチャレンジのモチベーションに合っている。
そのため、推論・API利用・RAGではTinySwallowを使い倒す。

一方で、初心者がいきなりTinySwallowをファインチューニング対象にすると、ライブラリ、トークナイザー、特殊トークン、変換周りで詰まる可能性がある。

そのため、ファインチューニング練習は情報量が多く、事例も豊富な `Qwen/Qwen2.5-1.5B-Instruct` に固定する。

TinySwallowはQwen2.5系のモデルを学生モデルとして使った流れに近いため、Qwen2.5でFTを練習することはTinySwallow理解にもつながる。

---

# 6. API利用方針

Codexは以下の方針に従うこと。

```text
Chat completion:
  OllamaのOpenAI互換APIを使う。
  エンドポイントは http://localhost:11434/v1/chat/completions を使う。
  Pythonでは openai パッケージを使い、base_url を http://localhost:11434/v1 にする。

Embedding:
  Ollamaの /api/embed を使う。
  モデルは bge-m3 に固定する。
  EmbeddingまでOpenAI互換APIに統一しようとしなくてよい。

原則:
  Chat生成はOpenAI互換API。
  EmbeddingはOllama native API。
  モデル選定に時間を使わない。
```

PythonでのOpenAI互換API呼び出しイメージ。

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M",
    messages=[
        {"role": "system", "content": "あなたは日本語で簡潔に答えるアシスタントです。"},
        {"role": "user", "content": "ローカルLLMとは何ですか？"},
    ],
)

print(response.choices[0].message.content)
```

Embedding呼び出しイメージ。

```python
import requests

response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "bge-m3",
        "input": "これはEmbeddingのテストです。",
    },
)
print(response.json())
```

---

# 7. 主要コマンド例

## TinySwallowをOllamaで起動する

```bash
ollama run hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M
```

## bge-m3を取得する

```bash
ollama pull bge-m3
```

## Qwen2.5 1.5B InstructをOllamaで起動する

Day 5でQwenと比較する場合に使う。
ただし、これは可能ならでよい。TinySwallow比較を優先する。

```bash
ollama run qwen2.5:1.5b-instruct
```

## llama.cpp serverを使う場合

```bash
brew install llama.cpp
llama-server -hf SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M
```

## Python仮想環境

```bash
mkdir local-llm-30days
cd local-llm-30days

python -m venv .venv
source .venv/bin/activate

pip install openai requests numpy
```

---

# 8. 環境ルート

## 第一候補: Mac / Apple Siliconの場合

```text
推論: Ollama
API: Ollama OpenAI互換API
Embedding: Ollama + bge-m3
FT候補: mlx-lm
バックアップ: Google Colab + Unsloth
```

## Windows + NVIDIA GPUの場合

```text
推論: Ollama
API: Ollama OpenAI互換API
Embedding: Ollama + bge-m3
FT候補: Unsloth / Transformers + PEFT
バックアップ: Google Colab + Unsloth
```

## GPUなし、または環境構築で詰まる場合

```text
推論: ローカルOllama
Embedding: ローカルOllama + bge-m3
FT: Google Colab + Unsloth
方針: ローカルにこだわりすぎず、30日完走を優先する
```

---

# 9. 推奨ディレクトリ構成

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
    eval_seed.jsonl
    train.jsonl
    valid.jsonl
    eval.jsonl

  finetune/
    env_smoke_result.md
    smoke_test_result.md
    adapter_smoke/
    tuned_adapter_v1/

  eval/
    questions.md
    materials.md
    ft_questions.md
    runs/
      day05_tinyswallow.md
      day05_qwen_base.md
      day20_rag_without.md
      day20_rag_with.md
      day27_qwen_base_ft.md
      day27_qwen_tuned_ft.md
      day27_qwen_base_general.md
      day27_qwen_tuned_general.md
      day28_tinyswallow_general.md
      day28_compare.md
      day29_final_outputs.md
    day05_model_compare.md
    day20_rag_eval.md
    day27_ft_eval.md
    day28_tinyswallow_vs_tuned_qwen.md
    final_eval.md

  next_challenge.md
```

---

# 10. 評価出力の保存ルール

評価に使ったモデル出力は、必ず `eval/runs/` に保存する。

理由は、Day 28やDay 29で再実行や配備作業に寄り道しないためである。

```text
Day 5:
  TinySwallowの出力 → eval/runs/day05_tinyswallow.md
  Qwen baseを比較した場合 → eval/runs/day05_qwen_base.md

Day 20:
  RAGなし出力 → eval/runs/day20_rag_without.md
  RAGあり出力 → eval/runs/day20_rag_with.md

Day 27:
  base QwenのFT評価出力 → eval/runs/day27_qwen_base_ft.md
  tuned QwenのFT評価出力 → eval/runs/day27_qwen_tuned_ft.md
  base Qwenの汎用評価出力 → eval/runs/day27_qwen_base_general.md
  tuned Qwenの汎用評価出力 → eval/runs/day27_qwen_tuned_general.md

Day 28:
  TinySwallowの汎用評価出力 → eval/runs/day28_tinyswallow_general.md
  比較メモ → eval/runs/day28_compare.md
  Qwen系の汎用評価出力は、原則としてDay 27で保存した出力を再利用する
  Day 27の保存が欠けている場合、その再実行はDay 28ではなくDay 29で行う

Day 29:
  最終比較に使った出力 → eval/runs/day29_final_outputs.md
  保存済みruns出力を再利用してよい
  再実行は不足分だけに限定する
```

---

# 11. 毎日のログ形式

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

# 12. 詰まった時のルール

```text
平日に詰まったら15分で切り上げる。
原因究明を続けず、詰まった内容をログに残す。
重い作業は土日祝に回す。
週次整理日であるDay 7 / Day 14は遅延吸収日を兼ねる。
ローカルFTで詰まったらColab + Unslothに逃げる。
TinySwallowのFTで詰まったら、Qwen2.5-1.5B-Instructで完走を優先する。
GGUF変換で詰まっても、最終評価ができていれば完走扱いにする。
完璧なモデル作成より、LLMの仕組み理解と一周体験を優先する。
```

---

# 13. Codexへの基本指示

Codexは以下を守ること。

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
- Chat生成はOllamaのOpenAI互換APIを使う
- EmbeddingはOllamaのbge-m3を使う
- READMEやログに残すべき内容も提案する
- 社外秘、個人情報、会社の機密情報をデータセットに入れないよう注意する
- Day 1で固定した eval/questions.md と eval/materials.md を評価時に必ず使う
- FTデータセットは messages 形式JSONLに固定する
- FT評価ケースは dataset/eval.jsonl 由来の held-out データから作る
- 評価出力は eval/runs/ に保存する
```

---

# 14. 日別計画

|    Day | 日付   | 曜日 | 学習テーマ                           | 具体的な学習手順                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 習得スキル                                                | 備考                                                                                                                                                                                                              |
| -----: | ---- | -- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  Day 0 | 7/13 | 月  | 環境ルート決定                         | 1. PCのチップとメモリを確認する。<br>2. Apple Silicon Macなら第一候補をMLXにする。<br>3. ローカルFTが重そうならGoogle Colab + Unslothをバックアップにする。<br>4. Ollama、Python、Git、VS Code/Codexの利用準備をする。<br>5. `local-llm-30days` リポジトリを作成する。                                                                                                                                                                                                                                                                                                                                  | 環境選定、学習ルート判断、開発環境準備                                  | すでに7/13を過ぎている場合は、Day 1開始前に30分だけ実施する。                                                                                                                                                                            |
|  Day 1 | 7/14 | 火  | TinySwallowをローカルで動かし、評価セットを固定する | 1. Day 0の未実施分として、PC環境、Ollama、Python、Gitを確認する。<br>2. `local-llm-30days` リポジトリと基本ディレクトリを作る。<br>3. `SakanaAI/TinySwallow-1.5B-Instruct-GGUF` をOllamaで実行する。<br>4. 評価用質問10問を `eval/questions.md` として固定する。<br>5. 評価素材を `eval/materials.md` として固定する。<br>6. 時間があれば、評価質問のうち2〜3問だけTinySwallowに投げてログを残す。                                                                                                                                                                                                                                      | ローカルLLM実行、Ollama基本操作、GGUFモデル利用、評価セット作成               | 平日1h。成果物：`logs/day01_first_run.md`, `eval/questions.md`, `eval/materials.md`。10問全部の実行はDay 5で回収してよい。                                                                                                             |
|  Day 2 | 7/15 | 水  | トークンの仕組み                        | 1. `llama-server` の `/tokenize` エンドポイント、またはHugging Face Tokenizer Playgroundで日本語と英語の短文を実際にトークン分割する。<br>2. 同じ意味の日英文でトークン数を比較する。<br>3. トークンが文字単位ではないことを整理する。<br>4. 日本語LLMでトークン効率が重要な理由を書く。                                                                                                                                                                                                                                                                                                                                           | トークン、語彙、入力長、コンテキスト長                                  | 平日1h。成果物：`notes/day02_tokens.md`                                                                                                                                                                                |
|  Day 3 | 7/16 | 木  | 生成パラメータ                         | 1. `ollama run` の対話中に `/set parameter temperature 0.1` のようにパラメータを変更できることを確認する。<br>2. 同じ質問をtemperature低め/高めで試す。<br>3. top_pの意味を調べる。<br>4. 事実回答、アイデア出し、文章生成で違いを見る。<br>5. 結果を表にする。                                                                                                                                                                                                                                                                                                                                                    | temperature、top_p、確率的生成、再現性                          | 平日1h。成果物：`logs/day03_generation_params.md`                                                                                                                                                                      |
|  Day 4 | 7/17 | 金  | 量子化の理解                          | 1. GGUF、Q4、Q5、Q8、F16を調べる。<br>2. TinySwallowの量子化版を確認する。<br>3. Q5_K_Mを使う理由を整理する。<br>4. 軽量化で何が犠牲になるかを書く。                                                                                                                                                                                                                                                                                                                                                                                                                              | 量子化、モデルサイズ、推論速度、品質劣化                                 | 平日1h。成果物：`notes/day04_quantization.md`                                                                                                                                                                          |
|  Day 5 | 7/18 | 土  | モデル比較                           | 1. TinySwallowに `eval/questions.md` の10問を投げる。<br>2. 質問に素材が必要な場合は `eval/materials.md` の固定素材を使う。<br>3. 出力を `eval/runs/day05_tinyswallow.md` に保存する。<br>4. 可能なら `ollama run qwen2.5:1.5b-instruct` でQwen2.5-1.5B-Instructにも同一セットを投げる。<br>5. Qwen比較をした場合、出力を `eval/runs/day05_qwen_base.md` に保存する。<br>6. 自然さ、正確さ、指示追従性を評価する。<br>7. TinySwallowの得意・不得意をまとめる。                                                                                                                                                                             | モデル比較、評価観点作成、日本語LLM観察                                | 休日3h。成果物：`eval/day05_model_compare.md`, `eval/runs/day05_tinyswallow.md`。Qwen比較は任意。                                                                                                                             |
|  Day 6 | 7/19 | 日  | Transformerと次トークン予測             | 1. LLMは次トークン予測モデルであることを理解する。<br>2. Attention、Transformer、事前学習、指示チューニングを調べる。<br>3. TinySwallowがInstruction-tunedモデルである意味を整理する。<br>4. 図解メモを作る。                                                                                                                                                                                                                                                                                                                                                                                       | Transformer、Attention、事前学習、Instruction tuning        | 休日3h。成果物：`notes/day06_transformer.md`                                                                                                                                                                           |
|  Day 7 | 7/20 | 月  | Week 1整理                        | 1. Day1〜6のメモを読み返す。<br>2. 用語集を作る。<br>3. 「ローカルでLLMを動かすとは何か」を文章化する。<br>4. README初版を書く。                                                                                                                                                                                                                                                                                                                                                                                                                                                | 技術用語の言語化、README作成、学習整理                               | 祝日3h。成果物：`README.md` 初版。遅れがある場合は遅延吸収日として使う。                                                                                                                                                                     |
|  Day 8 | 7/21 | 火  | Python環境構築とAPI疎通                | 1. Python仮想環境を作る。Day 0で済んでいる場合は確認だけでよい。<br>2. `openai` パッケージを入れる。<br>3. OllamaのOpenAI互換エンドポイント `http://localhost:11434/v1` に疎通確認する。<br>4. `src/`, `logs/`, `notes/` を作り、実行手順をREADMEに書く。                                                                                                                                                                                                                                                                                                                                            | Pythonプロジェクト構成、仮想環境、OpenAI互換APIの概念                   | 平日1h。成果物：リポジトリ初期構成、疎通確認スクリプト。以降のChat APIはOpenAI互換形式で書く。                                                                                                                                                         |
|  Day 9 | 7/22 | 水  | PythonからTinySwallowを呼ぶ          | 1. Ollamaを起動する。<br>2. OpenAI互換API `/v1/chat/completions` 経由でTinySwallowにリクエストを送る。<br>3. 標準入力から質問を受け取る。<br>4. 応答をターミナルに表示する。                                                                                                                                                                                                                                                                                                                                                                                                        | API呼び出し、OpenAI互換形式、ローカルLLMのプログラム利用                   | 平日1h。成果物：`src/ask_tinyswallow.py`                                                                                                                                                                               |
| Day 10 | 7/23 | 木  | 会話履歴                            | 1. `messages` 配列を作る。<br>2. user/assistant/system roleを整理する。<br>3. 会話履歴を持つCLIを作る。<br>4. 履歴が長い時の挙動を観察する。                                                                                                                                                                                                                                                                                                                                                                                                                             | Chat形式API、role、会話履歴、コンテキスト管理                         | 平日1h。成果物：`src/chat_cli.py`                                                                                                                                                                                      |
| Day 11 | 7/24 | 金  | ストリーミング応答                       | 1. OpenAI互換APIのstream出力を使う。<br>2. 応答を逐次表示する。<br>3. 一括表示と体感速度を比較する。<br>4. エラー処理を入れる。                                                                                                                                                                                                                                                                                                                                                                                                                                                | ストリーミング、CLI UX、例外処理                                  | 平日1h。成果物：`src/stream_chat.py`                                                                                                                                                                                   |
| Day 12 | 7/25 | 土  | 構造化出力                           | 1. TinySwallowにJSON形式で返すよう指示する。<br>2. 文章分類、要約、感情分類を試す。<br>3. JSON parse失敗ケースを観察する。<br>4. system promptで出力安定化を試す。                                                                                                                                                                                                                                                                                                                                                                                                                   | JSON出力、プロンプト設計、構造化レスポンス                              | 休日3h。成果物：`src/json_classifier.py`                                                                                                                                                                               |
| Day 13 | 7/26 | 日  | ミニアプリ作成                         | 1. 日本語文章を入力するCLIを作る。<br>2. 要約、改善、分類の3モードを作る。<br>3. TinySwallowを裏側で呼ぶ。<br>4. READMEに実行例を追記する。                                                                                                                                                                                                                                                                                                                                                                                                                                       | ローカルLLMアプリ化、CLI設計、プロンプト分岐                            | 休日3h。成果物：`src/text_tool.py`                                                                                                                                                                                     |
| Day 14 | 7/27 | 月  | Week 2整理                        | 1. PythonからLLMを使う流れを図解する。<br>2. Ollama、モデル、API、Pythonアプリの関係を書く。<br>3. 作ったスクリプトを整理する。<br>4. READMEに使い方を書く。                                                                                                                                                                                                                                                                                                                                                                                                                          | API利用の全体像理解、ドキュメント化                                  | 平日1h。成果物：`notes/day14_api_summary.md`。遅れがある場合は遅延吸収日として使う。                                                                                                                                                       |
| Day 15 | 7/28 | 火  | Embedding基礎                     | 1. Embeddingとは文章をベクトルにすることだと理解する。<br>2. 類似文章が近いベクトルになることを調べる。<br>3. Embeddingモデルは `bge-m3` に固定し、`ollama pull bge-m3` で取得する。<br>4. 日本語文章を5〜10個用意し、類似度検索の用途をメモする。                                                                                                                                                                                                                                                                                                                                                                    | Embedding、ベクトル、類似度検索                                 | 平日1h。成果物：`notes/day15_embedding.md`。モデル選定に時間を使わない。                                                                                                                                                              |
| Day 16 | 7/29 | 水  | ベクトル検索実装                        | 1. `bge-m3` をOllamaのembeddingエンドポイント `/api/embed` で使う。<br>2. 10個程度の文章をベクトル化する。<br>3. 質問文に近い文章を検索する。<br>4. スコア付きで検索結果を表示する。                                                                                                                                                                                                                                                                                                                                                                                                         | ベクトル検索、コサイン類似度、検索スコア                                 | 平日1h。成果物：`src/vector_search.py`                                                                                                                                                                                 |
| Day 17 | 7/30 | 木  | RAG全体像                          | 1. RAGを「検索→文脈注入→回答生成」に分けて理解する。<br>2. RAGとFTの違いを軽く整理する。<br>3. TinySwallowに検索結果を渡す設計を考える。<br>4. RAG構成図を書く。                                                                                                                                                                                                                                                                                                                                                                                                                           | RAG、外部知識、コンテキスト注入                                    | 平日1h。成果物：`notes/day17_rag_architecture.md`                                                                                                                                                                      |
| Day 18 | 7/31 | 金  | チャンク分割                          | 1. Markdownメモを用意する。<br>2. 300字、500字、1000字で分割する。<br>3. 検索しやすさの違いを見る。<br>4. チャンクサイズと検索精度の関係を書く。                                                                                                                                                                                                                                                                                                                                                                                                                                      | チャンク設計、検索単位、コンテキスト設計                                 | 平日1h。成果物：`src/chunk_text.py`                                                                                                                                                                                    |
| Day 19 | 8/1  | 土  | 最小RAG実装                         | 1. Markdown文書をチャンク化する。<br>2. `bge-m3` でEmbeddingして保存する。<br>3. 質問に近いチャンクを検索する。<br>4. 検索結果をTinySwallowに渡して回答させる。                                                                                                                                                                                                                                                                                                                                                                                                                     | RAG実装、検索結果のプロンプト注入、根拠付き回答                            | 休日3h。成果物：`rag/rag_qa.py`                                                                                                                                                                                        |
| Day 20 | 8/2  | 日  | RAG評価＋FT環境スモークテスト               | 【前半1.5h: RAG評価】<br>1. `eval/questions.md` からRAG向きの質問を選び、RAGなし/ありの回答を比較する。<br>2. 必要な素材は `eval/materials.md` を使う。<br>3. 結果を `eval/runs/day20_rag_without.md` と `eval/runs/day20_rag_with.md` に保存する。<br>4. 根拠に沿っているか確認し、間違い方を分類する。<br><br>【後半1.5h: FT環境疎通】<br>5. Colab + Unslothの公式LoRAノートブックを、サンプルデータのまま一度最後まで実行する。<br>6. Macの場合はmlx-lmのLoRAチュートリアルも試せる範囲で試す。<br>7. Day26で使う本命ルートを決める。<br>8. 詰まった場合はColab一本化を即決する。                                                                                                                   | RAG評価、根拠性、ハルシネーション観察、FT環境の事前検証                       | 休日3h。成果物：`eval/day20_rag_eval.md`, `finetune/env_smoke_result.md`。この日がFT失敗リスク対策の最重要日。                                                                                                                           |
| Day 21 | 8/3  | 月  | RAGとFTの使い分け                     | 1. RAGは知識を外から渡す方法だと整理する。<br>2. FTは振る舞いや形式を寄せる方法だと整理する。<br>3. 向いている用途を表にする。<br>4. FTで学習させたい振る舞いを決める。                                                                                                                                                                                                                                                                                                                                                                                                                                | RAG/FTの使い分け、学習対象の設計                                  | 平日1h。成果物：`notes/day21_rag_vs_finetune.md`                                                                                                                                                                       |
| Day 22 | 8/4  | 火  | FT基礎とDay20ノートブック読解              | 1. SFT、LoRA、QLoRA、adapter、mergeを調べる。<br>2. Day20で動かしたUnslothまたはMLXのノートブックを開く。<br>3. LoRA rank、learning rate、epoch、batch size、target modulesがどこで指定されているか確認する。<br>4. base model、dataset、trainer、adapter保存先がどこで指定されているか確認する。<br>5. Day26で自作データに差し替える時に変更する箇所をメモする。                                                                                                                                                                                                                                                                    | SFT、LoRA、QLoRA、adapter、FTノートブック読解、パラメータ理解            | 平日1h。成果物：`notes/day22_finetune_strategy.md`。Day26で触る箇所と触らない箇所を明確にする。                                                                                                                                            |
| Day 23 | 8/5  | 水  | FTデータセット設計                      | 1. 学習させたい振る舞いを1つ決める。例：文章を丁寧に改善する、要約する、業務メモ化する。<br>2. データ形式を `messages` 形式のJSONLに固定する。<br>3. system/user/assistantの役割を決める。<br>4. 商用LLMに `messages` 形式でデータ生成させるためのプロンプトを作る。                                                                                                                                                                                                                                                                                                                                                          | Chat形式dataset設計、JSONL設計、データ生成プロンプト設計                 | 平日1h。成果物：`dataset/dataset_spec.md`, `dataset/generate_prompt.md`。`instruction/input/output` 形式は使わない。                                                                                                            |
| Day 24 | 8/6  | 木  | シンセティックデータ生成①                   | 1. ChatGPT/Claude/Gemini等で、`messages` 形式JSONLの候補を30〜50件生成する。<br>2. 生成プロンプトを調整する。<br>3. 明らかに低品質な例を除外する。<br>4. 5件を評価用に分離する。                                                                                                                                                                                                                                                                                                                                                                                                          | シンセティックデータ生成、messages形式JSONL、品質確認、評価用データ分離           | 平日1h。成果物：`dataset/raw_generated_v0.jsonl`, `dataset/eval_seed.jsonl`。`eval_seed.jsonl` の5件はDay25で `dataset/eval.jsonl` に統合する。                                                                                   |
| Day 25 | 8/7  | 金  | シンセティックデータ生成②                   | 1. `messages` 形式のデータを100件前後まで増やす。<br>2. 重複、表記ゆれ、長すぎる出力を修正する。<br>3. train/valid/evalに分け、Day24の `eval_seed.jsonl` は `eval.jsonl` に統合する。<br>4. JSONLとして読み込めるか検証スクリプトを作る。検証にはtrainとevalでuser入力が重複していないかのリークチェックも含める。<br>5. `dataset/eval.jsonl` から10件を選び、user入力とreference出力を `eval/ft_questions.md` に転記して固定する。                                                                                                                                                                                                                         | データクリーニング、train/valid/eval分割、JSONL検証、データリーク防止、FT評価設計 | 平日1h。成果物：`dataset/train.jsonl`, `dataset/valid.jsonl`, `dataset/eval.jsonl`, `src/validate_jsonl.py`, `eval/ft_questions.md`。`eval/ft_questions.md` はタスク名ではなく、実際に投げるuser入力と参照用assistant出力を含める。                  |
| Day 26 | 8/8  | 土  | 自作データでのFT実行                     | 1. Day20で疎通済みのルート、MLXまたはColab + Unslothを使う。<br>2. Day22で確認した変更箇所を参考に、base model、dataset path、output pathを自作データ向けに差し替える。<br>3. Day25の `messages` 形式JSONLを読み込ませる。<br>4. 1エポックまたは少ないstepだけ回す。<br>5. loss、adapter生成、推論確認まで行う。                                                                                                                                                                                                                                                                                                          | 自作データでのLoRA実行、messages形式dataset読み込み、adapter生成、デバッグ   | 休日3h。成果物：`finetune/smoke_test_result.md`, `finetune/adapter_smoke/`。データ形式変換ではなく、読み込み確認に集中する。                                                                                                                    |
| Day 27 | 8/9  | 日  | 本番FT＋評価                         | 1. Day26で通った設定を使う。<br>2. 学習step、epoch、learning rateを決めて本番学習する。<br>3. base Qwenとtuned Qwenに `eval/ft_questions.md` の各user入力を投げる。<br>4. 出力を `eval/runs/day27_qwen_base_ft.md` と `eval/runs/day27_qwen_tuned_ft.md` に保存する。<br>5. `eval/ft_questions.md` のreference出力と比較する。<br>6. 余力があれば、base Qwenとtuned Qwenに `eval/questions.md` も投げ、`eval/runs/day27_qwen_base_general.md` と `eval/runs/day27_qwen_tuned_general.md` に保存する。<br>7. 良くなった点、悪くなった点、壊れた点を記録する。                                                                          | 本番LoRA/QLoRA、評価比較、ハイパーパラメータ観察                        | 休日3h。成果物：`finetune/tuned_adapter_v1/`, `eval/day27_ft_eval.md`, `eval/runs/day27_qwen_base_ft.md`, `eval/runs/day27_qwen_tuned_ft.md`。Day28でQwenを再実行しないため、可能ならこの日に汎用評価出力も保存する。ただしFT評価が必須で、汎用評価出力の保存は準必須。        |
| Day 28 | 8/10 | 月  | TinySwallowとの比較                 | 1. TinySwallowに `eval/questions.md` の同一質問を投げる。必要な素材は `eval/materials.md` を使う。<br>2. 出力を `eval/runs/day28_tinyswallow_general.md` に保存する。<br>3. base Qwenとtuned Qwenの汎用評価出力は、原則としてDay27の `eval/runs/day27_qwen_base_general.md` と `eval/runs/day27_qwen_tuned_general.md` を再利用する。<br>4. Day27に汎用評価出力を保存できていない場合は、平日1時間内でのFT環境の開き直しはせず、Qwen系の汎用比較はDay 29に回す。この日はTinySwallowと保存済み出力だけで比較する。<br>5. TinySwallowの自然さと、tuned Qwenのタスク特化を比較する。<br>6. FTで変わるもの・変わらないものを整理する。<br>7. GGUF変換やOllama配備は行わない。<br>8. 余力があれば、Day26〜27のスクリプトのモデル名を `SakanaAI/TinySwallow-1.5B-Instruct` に差し替えて数stepだけFTスモークを試す。  | モデル横断比較、FT効果の理解、同系統モデルへのFT転用観察                       | 平日1h。成果物：`eval/day28_tinyswallow_vs_tuned_qwen.md`, `eval/runs/day28_tinyswallow_general.md`, `eval/runs/day28_compare.md`。Day28は比較・執筆が主目的。tuned QwenをOllamaに載せる作業はしない。TinySwallow FTは余力課題であり、失敗しても本編の失敗扱いにしない。 |
| Day 29 | 8/11 | 火  | 最終評価と配備                         | 1. 必須タスクとして、`eval/questions.md` と `eval/materials.md` を使い、TinySwallow、base Qwen、tuned Qwenの汎用評価を行う。<br>2. `eval/ft_questions.md` のuser入力を使い、base Qwenとtuned QwenのFTタスク評価を行う。<br>3. 保存済みの `eval/runs/` 出力を再利用してよい。再実行は出力が不足しているケースだけに限定する。<br>4. FT評価では `eval/ft_questions.md` のreference出力と比較する。<br>5. 最終比較に使った出力を `eval/runs/day29_final_outputs.md` に保存する。<br>6. 最終評価を `eval/final_eval.md` にまとめる。<br>7. 任意タスクとして、残り時間でadapter mergeまたはGGUF変換を試す。<br>8. 任意タスクとして、Ollamaまたはllama.cppで使う流れを調べる。<br>9. READMEにローカルLLMとして使える状態をまとめる。 | 最終評価、モデル配備、GGUF/Ollama理解                             | 祝日3h。成果物：`eval/final_eval.md`, `eval/runs/day29_final_outputs.md`。GGUF変換は任意。最終評価が完了していれば完走扱い。                                                                                                                   |
| Day 30 | 8/12 | 水  | 総まとめ                            | 1. 30日間の成果物を整理する。<br>2. READMEを完成させる。<br>3. LLMの動作原理、RAG、FT、評価を自分の言葉でまとめる。<br>4. 次の30日チャレンジ案を書く。                                                                                                                                                                                                                                                                                                                                                                                                                                   | 技術理解の言語化、成果物整理、次アクション設計                              | 平日1h。成果物：完成版README、`next_challenge.md`                                                                                                                                                                          |

---

# 15. 今日 7/14(火) の現実的な運用

本日はすでにDay 1当日である。
Day 0を十分にできていない場合、今日だけは以下の短縮運用にする。

|  時間 | やること                                          |
| --: | --------------------------------------------- |
| 10分 | PC環境確認。Mac/メモリ/Python/Git/Ollamaの有無を見る        |
| 10分 | `local-llm-30days` リポジトリ作成、ディレクトリだけ作る         |
| 15分 | TinySwallowをOllamaで起動する                       |
| 15分 | `eval/questions.md` と `eval/materials.md` を作る |
| 10分 | 余ったら評価質問のうち2〜3問だけ投げる                          |

今日の成功条件は以下。

```text
TinySwallowが起動した
eval/questions.md を作った
eval/materials.md を作った
2〜3問だけでも回答ログを残した
```

10問全部投げられなくても問題ない。
Day 5で同一質問セットを使って回収する。

---

# 16. Day 20 FT環境スモーク成功条件

Day 20では以下を満たせば成功とする。

```text
ColabまたはMLXでサンプル学習が開始できた
lossが表示された
adapterらしき出力が生成された
学習済みadapterで簡単な推論ができた
Day26で使うルートを決めた
```

全部できなくても、以下が決まれば最低限OK。

```text
Day26はColab + Unslothで行く
または
Day26はMLXで行く
```

Day 20で重要なのは、FT環境の不確実性をDay 26まで持ち越さないことである。

---

# 17. 評価質問セット

## 17.1 `eval/questions.md`

この質問セットは、TinySwallow、Qwen、RAG、最終比較で共通して使う。
Day 1で固定し、Day 5 / Day 20 / Day 28 / Day 29で使い回す。

```md
# eval/questions.md

1. ローカルLLMとは何か、初心者向けに説明してください。
2. RAGとファインチューニングの違いを説明してください。
3. MATERIAL-001を3行で要約してください。
4. MATERIAL-002をビジネス向けに丁寧に書き換えてください。
5. 日本語LLMを使うメリットを説明してください。
6. temperatureを上げると何が変わりますか。
7. MATERIAL-003をJSON形式で分類してください。
8. MATERIAL-004からToDoを抽出してください。
9. MATERIAL-001だけを根拠に、AI導入時に注意すべきことを答えてください。
10. MATERIAL-001〜004だけを根拠に、Aチームの昨年度の残業削減率を答えてください。（素材に書かれていないため、「分からない」と答えられるかを見る質問）
```

## 17.2 `eval/materials.md`

```md
# eval/materials.md

## MATERIAL-001: 要約・根拠回答用文章

生成AIの導入は、単に便利なツールを配布するだけでは定着しない。  
現場の業務課題を把握し、どの作業にAIを使うと効果があるのかを具体化する必要がある。  
また、出力結果をどのように確認し、どの範囲まで自動化してよいかを決めることも重要である。  
そのためには、技術理解だけでなく、業務設計、評価、安全性、運用ルールをあわせて考える必要がある。

## MATERIAL-002: 丁寧な業務文への書き換え用文章

これ、今日中にざっくり見ておいて。  
無理なら明日の朝でもいいけど、遅れそうなら早めに言って。  
あと、気になるところがあれば適当にコメント入れといて。

## MATERIAL-003: JSON分類用文章

Aチームでは、議事録の要約に時間がかかっている。  
毎週の定例後に担当者が手作業で要点をまとめているが、ToDoの抜け漏れが発生することがある。  
まずはAIで議事録を要約し、ToDo候補を抽出するPoCを試したい。

## MATERIAL-004: ToDo抽出用の架空社内メモ

今日の打ち合わせでは、まず営業チームの問い合わせ対応フローを整理することになった。  
佐藤さんが今週中に既存FAQを確認する。  
田中さんは来週火曜までに問い合わせ分類のサンプルを20件用意する。  
藤田さんはAIで分類できそうかを確認し、次回の定例で簡単に共有する。  
ただし、顧客名や個人情報は検証データに入れない方針とする。
```

## 17.3 `eval/ft_questions.md`

このファイルは、FT評価用の固定ケースである。
Day 25で `dataset/eval.jsonl` から10件を選び、user入力とreference出力を転記する。

Day 27 / Day 29では、このuser入力をbase Qwenとtuned Qwenに投げ、reference出力と比較する。

```md
# eval/ft_questions.md

このファイルはFT評価用の固定ケースである。
Day 25で dataset/eval.jsonl から10件を選び、user入力とreference出力を転記する。
Day 27 / Day 29では、このuser入力をbase Qwenとtuned Qwenに投げ、reference出力と比較する。

## FT-EVAL-001

### user
...

### reference
...

## FT-EVAL-002

### user
...

### reference
...

## FT-EVAL-003

### user
...

### reference
...

## FT-EVAL-004

### user
...

### reference
...

## FT-EVAL-005

### user
...

### reference
...

## FT-EVAL-006

### user
...

### reference
...

## FT-EVAL-007

### user
...

### reference
...

## FT-EVAL-008

### user
...

### reference
...

## FT-EVAL-009

### user
...

### reference
...

## FT-EVAL-010

### user
...

### reference
...
```

---

# 18. FT用データセットの形式

FT用データセットは、最初から `messages` 形式JSONLに固定する。

`instruction/input/output` 形式は使わない。
Day 26で形式変換に時間を使わないためである。

JSONLの1行は以下の形式を基本とする。

```json
{"messages":[{"role":"system","content":"あなたは日本語の業務文を整えるアシスタントです。"},{"role":"user","content":"次の文章を丁寧な業務文に書き換えてください。\nこれ今日中にやっといて。無理なら早めに言って。"},{"role":"assistant","content":"本日中にご対応いただけますでしょうか。難しい場合は、早めにご共有いただけますと助かります。"}]}
```

---

# 19. シンセティックデータ生成プロンプト例

```md
あなたは日本語の業務文データセットを作るアシスタントです。

目的:
小型LLMをLoRAファインチューニングし、雑な日本語メモを丁寧で分かりやすい業務文に変換できるようにしたいです。

以下のJSONL形式で、30件のデータを作成してください。

形式:
- 1行に1 JSON object
- 各JSON objectは messages キーを持つ
- messages は system / user / assistant の3要素にする
- system は「あなたは日本語の業務文を整えるアシスタントです。」で統一する
- user には変換依頼と入力文を含める
- assistant には期待する出力文を入れる

条件:
- assistantの出力は自然な日本語にする
- userの入力にはカジュアル、曖昧、短すぎるメモを入れる
- assistantでは丁寧だが堅すぎないビジネス文にする
- 個人情報、会社名、実在人物名は入れない
- 内容は一般的な架空の業務にする
- Markdownのコードブロックは不要
- JSONとしてパースできる形にする

例:
{"messages":[{"role":"system","content":"あなたは日本語の業務文を整えるアシスタントです。"},{"role":"user","content":"次の文章を丁寧な業務文に書き換えてください。\nこれ今日中にやっといて。無理なら早めに言って。"},{"role":"assistant","content":"本日中にご対応いただけますでしょうか。難しい場合は、早めにご共有いただけますと助かります。"}]}
```

---

# 20. `validate_jsonl.py` の検証要件

Day 25で作る `src/validate_jsonl.py` は、最低限以下を確認する。

```text
各行がJSONとしてパースできる
各行に messages キーがある
messages が list である
system / user / assistant が含まれる
assistant の content が空でない
user の content が空でない
train と eval で user content が完全一致していない
```

リークチェックの目的は、trainとevalにほぼ同じ入力が入って評価が甘くなることを避けるためである。
厳密な類似度チェックまでは必須ではない。まずは完全一致チェックでよい。

---

# 21. Day 22 FTノートブック読解メモのテンプレート

```md
# Day 22 FTノートブック読解メモ

## Day20で使ったルート
- Colab + Unsloth / MLX

## 変更する箇所
- base model:
- dataset path:
- output adapter path:
- learning rate:
- epoch / max steps:
- batch size:
- LoRA rank:
- target modules:

## Day26で触らない箇所
-

## 分からないが今は深追いしない箇所
-
```

---

# 22. 30日後に説明できるべきこと

| 観点          | 説明できるべきこと                          |
| ----------- | ---------------------------------- |
| ローカルLLM     | クラウドAPIではなく、自分のPC上でLLMを動かす意味       |
| TinySwallow | Sakana AIの日本語向け小型LLMとしての位置づけ       |
| Qwen2.5     | FT練習用モデルとして使う理由                    |
| トークン        | LLMが文字ではなくトークン単位で扱うこと              |
| 生成パラメータ     | temperatureやtop_pで出力が変わる理由         |
| 量子化         | モデルを軽くして動かす仕組みとトレードオフ              |
| GGUF        | ローカル推論で使われるモデル形式                   |
| OpenAI互換API | OllamaをOpenAI形式で呼ぶ意味               |
| Embedding   | 文章をベクトル化して検索する意味                   |
| bge-m3      | 日本語文書のEmbeddingモデルとして使う理由          |
| RAG         | 検索した外部知識をLLMに渡す仕組み                 |
| FT          | モデルの振る舞いを学習で寄せる方法                  |
| LoRA        | 全重みを更新せず、追加のadapterを学習する考え方        |
| QLoRA       | 量子化モデルを使って省メモリでFTする考え方             |
| データリーク      | trainとevalに同じ入力があると評価が甘くなる理由       |
| 評価          | 同一質問セットと同一素材でbase/tuned/RAGを比較する方法 |

---

# 23. 完走条件

この30日チャレンジは、以下ができていれば完走とする。

```text
TinySwallowをローカルで動かした
eval/questions.md と eval/materials.md を固定した
PythonからTinySwallowをOpenAI互換APIで呼べた
bge-m3でEmbeddingを作った
最小RAGを作った
RAGあり/なしを比較した
Day20でFT環境スモークを行い、Day26のルートを決めた
messages形式JSONLでFTデータを作った
validate_jsonl.pyでJSONL検証と簡易リークチェックを行った
dataset/eval.jsonl 由来の固定FT評価ケースを作った
Qwen2.5でLoRA/QLoRAを一度は回した
base Qwenとtuned Qwenを比較した
TinySwallow、base Qwen、tuned Qwenの違いを説明した
READMEに30日間の成果をまとめた
```

以下は任意であり、未達でも完走扱いとする。

```text
TinySwallow自体のFT
adapter merge
GGUF変換
Ollamaへのtuned model登録
本格的なUI作成
本番品質のRAG
```

---

# 24. 次の30日チャレンジ候補

今回の30日が終わった後は、120日計画の次ステップとして以下へ進む。

```text
日本語ナレッジ検索基盤30日チャレンジ
```

主な内容。

```text
VectorDB
RAG実践
GraphDB基礎
GraphRAG入口
検索評価
```

ただし、GraphDBは深追いせず、VectorDB/RAGを中心に進める。

---

# 25. この30日チャレンジの最終方針

```text
TinySwallowでローカルLLMを使い倒す。
OpenAI互換APIでコード資産化する。
bge-m3でEmbeddingを固定し、RAGまで迷わず進める。
FTはQwen2.5で確実に一周する。
FT環境はDay20で先に疎通する。
評価質問と評価素材はDay1で固定し、最後まで使い回す。
評価出力はeval/runs/に保存する。
FTデータはmessages形式JSONLに固定する。
FT評価ケースはdataset/eval.jsonl由来で固定する。
Day22で実物ノートブックを読み、Day26で触る箇所を明確にする。
Day27で可能ならQwenの汎用評価出力も保存し、Day28は比較・執筆に集中する。
GGUF変換やTinySwallow FTは余力課題にする。
```

この計画では、30日後に完璧なモデルを作ることではなく、LLM・RAG・FT・評価を実装感を持って説明できるようになることを最優先にする。
