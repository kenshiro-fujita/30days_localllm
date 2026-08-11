# Day22 ファインチューニング戦略メモ

## 今日の目的

Day20で動かしたMLX-LMのQLoRA設定を読み解き、Day26で自作データを使う際に変更する箇所と、最初は変更しない箇所を整理する。

## 基礎用語

### SFT

正解例を示し、「この入力にはこのように答える」という振る舞いを学ばせる教師ありファインチューニング。

### LoRA

ベースモデルの大部分を固定し、少数の追加パラメータだけを学習する方法。フルファインチューニングより、必要なメモリ、計算量、保存容量を抑えられる。

### QLoRA

量子化して軽量化したベースモデルを固定し、LoRAの追加パラメータを学習する方法。量子化の主な目的は、学習効果を強めることではなく、ベースモデルのメモリ使用量を減らすこと。

### adapter

LoRAで学習した差分を保存した小さなパーツ。基本的に学習時のベースモデルに対応しており、構造の異なるモデルへ自由に付け替えられるものではない。

### merge

adapterの学習結果をベースモデルへ統合する処理。Day26ではadapterの生成と推論確認を優先し、mergeは行わない。

## Day20で使ったルート

- 実行環境：Mac
- 学習ツール：MLX-LMの`mlx_lm.lora`
- ベースモデル：`models/RLT-7B-4bit`
- 学習方式：4bit量子化モデルに対するLoRA（QLoRA）
- データ形式：`messages`形式のJSONL
- adapter保存先：`finetune/day20_mlx_smoke_adapter`
- 結果：1 iterationの学習、adapter保存、adapter付き推論まで完了

## Day20の主要設定

| 設定 | 値 | 意味 |
| --- | ---: | --- |
| learning rate | `1e-5` | 1回の更新でパラメータを動かす大きさ |
| iterations | `1` | パラメータを更新する回数 |
| batch size | `1` | 1回の更新でまとめて処理するデータ数 |
| LoRA rank | `8` | adapterが表現できる変化の幅に関わる値 |
| num layers | `4` | LoRA学習の対象にする層数 |
| max sequence length | `128` | 1件の学習データで扱う最大トークン数 |
| mask prompt | 有効 | systemとuserをlossの対象から外し、assistant回答を中心に学習する |
| target modules | 明示指定なし | MLX-LMの標準設定に任せる |

## lossとは

lossは、モデルの予測と正解例のズレを数値化したもの。

- Train loss：学習に使っているデータでのズレ
- Val loss：学習には使わない検証データでのズレ
- Train lossだけが下がり、Val lossが悪化する場合は、学習データへの過学習が疑われる
- Day20は1 iterationだけなので、lossの改善傾向や回答品質は評価できない


## Day26で必ず変更する箇所

- `data`
  - Day25で作成する自作データセットのディレクトリへ変更する。
- `adapter-path`
  - Day20の結果を上書きしないよう、Day26専用の保存先へ変更する。

## データを確認して変更を検討する箇所

- `iters`
  - Day20の`1`は動作確認用。Day26では少ない回数から始める。
- `max-seq-length`
  - 自作データが128トークンを超える場合は、回答が途中で切れない値へ変更する。

## Day26の初回は変更しない箇所

- ベースモデル：`models/RLT-7B-4bit`
- batch size：`1`
- learning rate：`1e-5`
- LoRA rank：`8`
- num layers：`4`
- `mask-prompt`：有効
- target modules：明示指定せず、MLX-LMの標準設定を使う

最初は変更点を絞り、問題が起きたときに原因を切り分けやすくする。

## Day26では触らない箇所

- adapterのmerge
- MLX-LM内部の実装
- target modulesの細かな最適化
- 大規模なハイパーパラメータ探索

## Day26で確認する流れ

1. 自作JSONLを読み込めるか確認する。
2. 少ないiterationで学習する。
3. Train lossとVal lossが記録されることを確認する。
4. adapterが指定先へ保存されることを確認する。
5. ベースモデルとadapterを組み合わせて推論する。

## 今の理解

SFTは正解例から振る舞いを学ばせる方法です。QLoRAでは、量子化したベースモデルを固定し、小さなadapterを学習します。Day26では動作確認済みの条件をできるだけ維持し、自作データと保存先を主に差し替えます。