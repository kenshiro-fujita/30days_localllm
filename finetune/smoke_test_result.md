# Day26 自作データによるQLoRAスモークテスト

## 結論

Mac上のMLX-LMとRLT-7B 4bitを使い、Day25で作成した`messages`形式JSONLの読み込み、1 iterationのLoRA学習、adapter保存、adapter付き推論まで完了した。

今回は学習経路の疎通確認が目的であり、回答品質の改善は評価しない。本番学習とbaseモデルとの比較はDay27で行う。

## 学習前のデータ検証

```text
検証成功
train: 80件
valid: 10件
eval: 10件
分割間のuser入力の完全一致: なし
```

最長行はtrainが1821文字、validが1475文字だった。トークン数とは一致しないが、Day20の`max-seq-length 128`では短い可能性があるため、今回は`512`へ変更した。

## 実行条件

```bash
mlx_lm.lora \
  --model models/RLT-7B-4bit \
  --train \
  --data dataset \
  --fine-tune-type lora \
  --iters 1 \
  --batch-size 1 \
  --num-layers 4 \
  --max-seq-length 512 \
  --steps-per-report 1 \
  --steps-per-eval 1 \
  --val-batches 1 \
  --mask-prompt \
  --adapter-path finetune/adapter_smoke
```

## 学習結果

```text
Trainable parameters: 0.038% (2.884M/7615.617M)
Iter 1: Val loss 1.895, Val took 2.974s
Iter 1: Train loss 1.085, Learning Rate 1.000e-05, It/sec 0.417, Tokens/sec 53.758, Trained Tokens 129, Peak mem 5.378 GB
Saved final weights to finetune/adapter_smoke/adapters.safetensors.
```

- ベースモデル本体は固定し、全体の0.038%に当たる約288万のLoRAパラメータを学習した。
- 1 iterationだけなので、Train lossとVal lossの大小から性能や過学習は判断しない。
- 約11MBの`adapters.safetensors`と`adapter_config.json`が保存された。

## adapter付き推論

入力：

```text
次の会議メモを、要点・決定事項・次の行動に整理してください。会議メモ：新しい問い合わせ管理ツールを10月から試験導入する。担当は田中さん。9月20日までに候補を3製品へ絞り、次回会議で比較する。
```

出力：

```text
要点：
- 10月から新しい問い合わせ管理ツールの試験導入を開始する。
- 担当者は田中さん。
- 候補製品を3つまで絞り込む。
- 候补製品の比較は9月20日までに行う。

決定事項：
- 新しい問い合わせ管理ツールの試験導入を10月から開始することを決定。
- 田中さんが担当者となる。
- 候補製品を3つまで絞り込む。

次の行動：
- 9月20日までに3つの候補製品を絞り込む。
- 前提条件：候補製品の比較を9月20日までに行う。
```

- adapterを読み込んだ推論は完了した。
- `候补`という不自然な字が混ざった。
- 元メモの「9月20日までに候補を絞り、次回会議で比較する」を、「比較も9月20日まで」と誤って整理した。
- 1 iterationの結果なので、形式が出たことだけでFTの効果とは判断しない。

## Day27へ引き継ぐこと

- 今回通った設定を土台に本番学習を行う。
- `eval/ft_questions.md`の同じ入力をbaseモデルとtunedモデルへ渡す。
- reference出力と比較し、形式、情報保持、誤情報の観点から評価する。
