# Day20 ファインチューニング環境スモークテスト

## 結論

Mac上のMLX-LMを使い、RLT-7B 4bitでQLoRAのデータ読み込み、検証、1ステップ学習、アダプター保存、アダプター付き推論まで完了した。Day26の本命ルートはMac＋MLX-LMとする。Colabへの一本化は不要と判断した。

## 環境

- Python: 3.12.13
- mlx-lm: 0.31.3
- ベースモデル: `models/RLT-7B-4bit`
- データ形式: `messages`形式のJSONL
- 学習データ: 3件
- 検証データ: 1件
- 学習方式: 4bit量子化モデルに対するLoRA（QLoRA）

## 実行条件

```bash
mlx_lm.lora \
  --model models/RLT-7B-4bit \
  --train \
  --data finetune/day20_sample_data \
  --fine-tune-type lora \
  --iters 1 \
  --batch-size 1 \
  --num-layers 4 \
  --max-seq-length 128 \
  --steps-per-report 1 \
  --steps-per-eval 1 \
  --val-batches 1 \
  --mask-prompt \
  --adapter-path finetune/day20_mlx_smoke_adapter
```

## 学習結果

```text
Trainable parameters: 0.038% (2.884M/7615.617M)
Iter 1: Val loss 1.910, Val took 1.677s
Iter 1: Train loss 1.367, Learning Rate 1.000e-05, It/sec 0.420, Tokens/sec 6.714, Trained Tokens 16, Peak mem 4.493 GB
Saved final weights to finetune/day20_mlx_smoke_adapter/adapters.safetensors.
```

- 学習対象は全体の0.038%、約288万パラメータだった。
- 1ステップのため、lossの改善や回答品質は評価しない。
- ピークメモリ約4.5GBで完了した。
- 約11MBの`adapters.safetensors`と、実行条件を記録した`adapter_config.json`が保存された。

## アダプター付き推論

```bash
mlx_lm.generate \
  --model models/RLT-7B-4bit \
  --adapter-path finetune/day20_mlx_smoke_adapter \
  --prompt "朝の挨拶をしてください。" \
  --max-tokens 100
```

出力:

```text
お早朝お疲れさまでした。朝の挨拶をさせていただきます。良い一日になりますように。
```

- Prompt: 36 tokens、30.365 tokens/sec
- Generation: 24 tokens、37.452 tokens/sec
- Peak memory: 4.429GB

「お早朝」という不自然な表現が出たが、1ステップのスモークテストなので品質改善は目的ではない。アダプターを読み込み、推論できたことを成功条件とする。

## Day26へ向けた判断

- 本命ルート: Mac＋MLX-LM＋RLT-7B 4bit＋QLoRA
- データ形式: Day23〜25で作る`messages`形式JSONLをそのまま利用する
- 変更箇所: model、data、adapter-path、itersなどの学習条件
- 維持する方針: まずbatch size 1、少ないiteration、少ない学習レイヤーで疎通させる
- Colab: MLX経路で解決できない問題が出た場合の予備ルート

