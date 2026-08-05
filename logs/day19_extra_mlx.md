# Day19番外編 MLXで7Bモデルを動かす

学習日: 2026-08-04

## 目的

Apple Silicon向けのMLXを導入し、Sakana AIが公開している以下の7Bモデルを4bit量子化してローカルで動かす。

- `SakanaAI/EvoLLM-JP-v1-7B`
- `SakanaAI/RLT-7B`

## 環境

- MacBook Pro
- Apple M2 Pro（10コア）
- メモリ: 32GB
- 作業開始時の空き容量: 149GiB
- Python: 3.12.13（MLX専用の`.venv-mlx`）
- `mlx-lm`: 0.31.3
- `mlx`: 0.32.0

既存の`.venv`はPython 3.14.6だった。新しすぎるPythonによる互換性問題を避けるため、既存環境は変更せず、`uv`でPython 3.12の専用環境を作った。

## 環境構築

```bash
deactivate
uv venv .venv-mlx --python 3.12
source .venv-mlx/bin/activate
uv pip install mlx-lm
mlx_lm.convert --help
```

次回以降は、リポジトリのルートで以下を実行すればMLX専用環境へ入れる。

```bash
source .venv-mlx/bin/activate
```

## EvoLLM-JP-v1-7Bの変換

```bash
mlx_lm.convert \
  --hf-path SakanaAI/EvoLLM-JP-v1-7B \
  --mlx-path models/EvoLLM-JP-v1-7B-4bit \
  --quantize \
  --q-bits 4
```

初回は12.4GBをダウンロードし、14.5GBを再構築して量子化した。しかし、保存時に`.gitattributes`、`LICENSE`、`README.md`がキャッシュにないという`IncompleteSnapshotError`が発生した。

不足ファイルだけを取得した。

```bash
hf download SakanaAI/EvoLLM-JP-v1-7B \
  .gitattributes LICENSE README.md
```

その後、同じ`mlx_lm.convert`を再実行して保存に成功した。変換後の容量は3.8GBだった。

## RLT-7Bの変換

```bash
mlx_lm.convert \
  --hf-path SakanaAI/RLT-7B \
  --mlx-path models/RLT-7B-4bit \
  --quantize \
  --q-bits 4
```

初回は13.2GBをダウンロードし、15.2GBを再構築して量子化した。EvoLLM-JPと同様に、保存時に`.gitattributes`と`README.md`が不足して停止した。

```bash
hf download SakanaAI/RLT-7B .gitattributes README.md
```

不足ファイルを補完後、同じ変換を再実行して成功した。変換後の容量は4.0GBだった。

このエラーはユーザー操作ではなく、`mlx-lm`が最初に取得するファイルと、保存時に完全なスナップショットとして要求するファイルの噛み合わせによって発生した。

## 同じ質問で動作確認

両モデルに次の質問を与えた。

```text
ローカルLLMを使う利点と注意点を、日本語で3つずつ簡潔に説明してください。
```

EvoLLM-JPの実行コマンド:

```bash
mlx_lm.generate \
  --model models/EvoLLM-JP-v1-7B-4bit \
  --prompt "ローカルLLMを使う利点と注意点を、日本語で3つずつ簡潔に説明してください。" \
  --max-tokens 300
```

RLT-7Bの実行コマンド:

```bash
mlx_lm.generate \
  --model models/RLT-7B-4bit \
  --prompt "ローカルLLMを使う利点と注意点を、日本語で3つずつ簡潔に説明してください。" \
  --max-tokens 300
```

## 実測結果

### EvoLLM-JP-v1-7B 4bit

- Prompt: 45 tokens、19.662 tokens/sec
- Generation: 300 tokens、39.777 tokens/sec
- Peak memory: 4.256GB
- 4bitモデル容量: 3.8GB
- 日本語で箇条書きにし、3つずつ答えようとした
- 300トークン上限に達し、注意点の途中で終了した
- 「クラウドLLMより速い」「入力をローカルストレージへ保存する」など、条件不足または不正確な説明があった

### RLT-7B 4bit

- Prompt: 58 tokens、52.261 tokens/sec
- Generation: 300 tokens、38.841 tokens/sec
- Peak memory: 4.476GB
- 4bitモデル容量: 4.0GB
- 今回はEvoLLM-JPより自然で具体的な日本語回答だった
- 300トークン上限に達し、3つ目の注意点の途中で終了した
- 応答速度に関する説明などは、利用環境による条件を補って読む必要がある

## Git管理

変換後モデルと仮想環境を誤ってコミットしないよう、`.gitignore`へ以下を追加した。

```text
.venv-mlx/
models/
```

## 今回の結論

M2 Pro・32GBでは、4bit化した7Bモデルを最大メモリ約4.3〜4.5GB、生成速度約39 tokens/secで動かせた。MLXを使うことで、TinySwallowより大きいモデルでも待ち時間を強く感じずに試せることが分かった。今回の1問ではRLT-7Bの回答が良かったが、汎用的な優劣は複数の質問で評価する必要がある。

## OllamaとMLXの関係を整理

MLXモデルの変換後に`ollama list`を実行したところ、表示されたのは従来の3モデルだけだった。

```text
bge-m3:latest
qwen2.5:1.5b-instruct
hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M
```

EvoLLM-JPとRLT-7Bが表示されなかったことで、OllamaとMLXは同じモデル一覧を共有しない、独立した実行環境だと理解した。

```text
Ollama
├─ TinySwallow（GGUF）
├─ Qwen2.5（GGUF）
└─ bge-m3

MLX + mlx-lm
├─ EvoLLM-JP-v1-7B（MLX形式）
└─ RLT-7B（MLX形式）
```

Ollamaは、モデルの取得、一覧管理、対話、API公開までをまとめて扱うローカルLLM実行ツールである。MLXはApple Silicon向けの機械学習基盤であり、`mlx-lm`を使うことでLLMの変換、量子化、推論、学習を扱いやすくできる。

今回作成したMLXモデルは`ollama run`ではなく、次のコマンドで呼び出す。

```bash
mlx_lm.chat --model models/RLT-7B-4bit
mlx_lm.chat --model models/EvoLLM-JP-v1-7B-4bit
```

単発生成では、`mlx_lm.generate`の`--model`を差し替えるだけで呼び分けられる。同じ質問を複数モデルへ順番に与える比較プログラムも作成できる。Ollamaモデルまで一緒に比較する場合は、MLXのPython APIとOllamaのHTTP APIという呼び出し方の違いを比較プログラム側で吸収する必要がある。

## MLXと学習

MLXは完成済みモデルの推論だけでなく、Apple Silicon上でLoRAファインチューニングを行う用途にも使える。

学習には大きく次の種類がある。

- 事前学習: モデルをほぼゼロから育てる
- フルファインチューニング: 元モデルの全パラメータを更新する
- LoRA: 元モデルを残し、小さな追加パラメータを学習する

今回のM2 Pro・32GBと30日チャレンジの目的では、事前学習や7Bモデルのフルファインチューニングではなく、LoRAが現実的である。Ollamaは主に完成済みモデルを手軽に利用する役割で、学習処理はMLXなどで行う。必要に応じて、MLXで学習した成果を統合・変換してOllamaで利用する構成も考えられる。

今回の理解を一文にすると、Ollamaは完成したLLMを手軽に使う環境で、MLXはApple Silicon上でLLMの推論、量子化、LoRA学習まで扱える基盤である。
