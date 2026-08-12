# Day26 学習メモ：自作データでのファインチューニング実行

## 今日のテーマ

Day25で作った自作データをMLX-LMへ読み込ませ、少量のQLoRA学習からadapter付き推論まで一周する。

## 今日理解したこと

- QLoRAでは7Bモデル全体を学習し直すのではなく、量子化したベースモデルを固定し、追加したLoRA adapterの差分パラメータを学習する。
- `Trainable parameters: 0.038% (2.884M/7615.617M)`は、約76億パラメータのうち学習対象が約288万、全体の0.038%だったことを表す。
- adapterはベースモデル全体ではなく、今回学習した差分を保存する。生成されたファイルは約11MBだった。
- `max-seq-length`は1件の学習で扱う最大トークン長。文字数とトークン数は同じではないが、データの長さを見て設定を検討する必要がある。
- Train lossは学習データ上のズレ、Val lossは学習に使わない検証データ上のズレである。
- 1 iterationだけの結果では、lossの改善傾向、過学習、回答品質は判断できない。
- 今回成功したのは、自作データの読み込み、LoRA学習、adapter保存、adapter付き推論という一連の経路である。
- 推論できることと、正確で高品質な回答になることは別である。実際の出力では文字の混在、期限の誤読、次の行動の欠落があった。

## 今日出てきた重要用語

- trainable parameters：学習によって更新されるパラメータ
- adapter：LoRAで学習した差分を保存する小さなパーツ
- iteration：パラメータを更新する回数
- max sequence length：1件のデータで扱う最大トークン数
- Train loss：学習データに対する予測と正解のズレ
- Val loss：検証データに対する予測と正解のズレ
- smoke test：品質を作り込む前に、一連の処理が通るかを小さい条件で確認する試験

## 実行したコマンドと、その意味

```text
python src/validate_jsonl.py dataset/train.jsonl dataset/valid.jsonl dataset/eval.jsonl
```

train・valid・evalが想定した`messages`形式で、分割間にuser入力の完全一致がないことを再確認した。

```text
wc -L dataset/train.jsonl dataset/valid.jsonl
```

各JSONLの最長行の文字数を調べ、`max-seq-length`を検討する材料にした。

```text
mlx_lm.lora --model models/RLT-7B-4bit --train --data dataset ...
```

自作データを使って1 iterationだけLoRA学習し、lossの出力とadapterの保存を確認した。

```text
ls -lh finetune/adapter_smoke
```

`adapter_config.json`と約11MBの`adapters.safetensors`が生成されたことを確認した。

```text
mlx_lm.generate --model models/RLT-7B-4bit --adapter-path finetune/adapter_smoke ...
```

ベースモデルへ学習済みadapterを組み合わせ、未使用の会議メモで推論できることを確認した。

## 今日作成したもの

- `finetune/adapter_smoke/`：1 iterationで学習したLoRA adapter
- `finetune/smoke_test_result.md`：設定、loss、推論結果、観察点の記録

コマンドの実行と結果確認はユーザーが行い、Codexは実行手順、設定値、結果の読み方を案内した。

## まだ曖昧なこと

- 80件のデータを何iterationまたは何epoch学習させると適切か
- Train lossとVal lossが本番学習でどのように変化するか
- 形式への追従と、元メモの情報を正確に保つ能力がそれぞれどの程度改善するか

## 自分の言葉でのまとめ

今回学習したのは7Bモデル全体ではなく、ごく一部の差分です。表示された0.038%が学習対象で、その結果がadapterとして保存されました。今回は品質改善の確認ではなく、自作データで学習から推論まで通ることを確認できました。
