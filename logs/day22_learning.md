# Day22 学習メモ：FT基礎とMLX-LM設定の読解

## 今日のテーマ

SFT、LoRA、QLoRA、adapter、mergeの違いを理解し、Day20で動かしたMLX-LMの設定から、Day26で変更する箇所と維持する箇所を整理する。

## 今日理解したこと

- SFTは、入力と正解例を示し、「この入力にはこのように答える」という振る舞いを学ばせる方法です。
- LoRAはモデル全体ではなく、追加した少数のパラメータを学習するため、計算量や保存容量を抑えられます。
- QLoRAは、量子化したベースモデルを固定してLoRAを行う方法です。量子化の目的は学習の影響を強めることではなく、主にメモリ使用量を減らすことです。
- adapterは学習した差分です。任意のモデルへ自由に付けられるものではなく、基本的に学習時のベースモデルや構造に対応します。
- mergeはadapterの差分をベースモデルへ統合する処理です。Day26では行いません。
- lossはモデルの予測と正解例のズレを数値化したものです。Train lossは学習データ、Val lossは未学習の検証データに対するズレです。
- 1 iterationだけではlossの改善傾向や回答品質は評価できません。Day20では、学習処理が動いてlossを計算できたことが確認点でした。
- `--mask-prompt`はsystemとuserを入力文脈として残しながら、主にassistantの回答部分をlossの計算対象にします。
- `max-seq-length`が短すぎて正解例が途中で切れると、半端な出力を正解として学ぶ可能性があります。
- 初回実行では変更点を絞ると、問題が起きた際に原因を切り分けやすくなります。

## 今日出てきた重要用語

- SFT：正解例を使う教師ありファインチューニング
- LoRA：少数の追加パラメータだけを学習する方法
- QLoRA：量子化モデルをベースに行うLoRA
- adapter：LoRAで学習した差分パーツ
- merge：adapterをベースモデルへ統合する処理
- loss：モデルの予測と正解例のズレ
- learning rate：1回の更新でパラメータを動かす大きさ
- iteration：パラメータを更新した回数
- epoch：学習データ全体を一巡した回数
- batch size：1回の更新でまとめて処理するデータ数
- LoRA rank：adapterが表現できる変化の幅に関わる値
- target modules：LoRAを適用する部品の種類

## 確認した設定と、その意味

- `--model models/RLT-7B-4bit`：ベースモデルを指定します。
- `--data finetune/day20_sample_data`：学習用・検証用JSONLの場所を指定します。
- `--adapter-path finetune/day20_mlx_smoke_adapter`：adapterの保存先を指定します。
- `--iters 1`：Day20では動作確認のため、更新を1回だけ行いました。
- `--batch-size 1`：1件ずつ処理し、メモリ使用量を抑えました。
- `--num-layers 4`：LoRA学習の対象を末尾側の4層に絞りました。
- `--max-seq-length 128`：1件あたり最大128トークンに制限しました。
- `--mask-prompt`：assistant回答を中心に学習する設定です。
- learning rateはMLX-LMの既定値`1e-5`、LoRA rankは既定値`8`でした。
- target modulesは明示指定せず、MLX-LMの標準設定に任せました。

既存ファイルを確認するためのコマンド操作はCodex側で行い、ユーザーは設定の意味の確認と戦略メモの作成を行いました。

## まだ曖昧なこと

- iteration数やlearning rateを、実際のlossと出力からどう調整するか
- 自作データに必要な`max-seq-length`をどう決めるか
- LoRA rankを変更した場合に、品質、計算量、adapterサイズが実際にどう変わるか
- MLX-LMが標準設定でLoRAを適用するtarget modulesの詳細

これらはDay25のデータ確認と、Day26〜27の学習・評価で確かめる。

## 自分の言葉でのまとめ

SFTは正解例から振る舞いを学ばせる方法です。QLoRAでは、量子化して軽くしたベースモデルを固定し、小さなadapterを学習します。Day26では一度に多くの条件を変えず、自作データとadapter保存先を主に差し替え、少ないiterationで動作を確認します。
