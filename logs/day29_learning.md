# Day29 学習メモ：最終評価と配備状態の整理

## 今日のテーマ

保存済みの評価出力を再利用してTinySwallow、base Qwen、tuned Qwenを最終比較し、FTの効果と副作用、現在の配備状態を整理する。

## 今日理解したこと

- 評価出力を保存しておけば、モデルを毎回再実行せず、同じ出力を使って比較できる。
- モデル別に分かれた長い出力は読み比べにくい。質問単位で各モデルを横並びにすると差を追いやすい。
- 全件を毎回人間が読むのは現実的ではない。明確な誤答、形式違反、入力にない情報、途中終了を先に整理し、代表ケースだけ確認する方法が使える。
- tuned Qwenはbase Qwenのシンプルな上位互換ではなかった。
- FT後は入力情報を素直に保持し、大きな捏造が減ったケースがあった。
- 一方で、指定した3区分を守れないケースや、学習データ由来の表現が別の質問にも現れる副作用があった。
- Train lossの低下と、実用上の回答品質の改善は同じではない。
- MLX-LMでbase modelとadapterを統合し、llama.cppでGGUFへ変換して、Ollamaへ4bit量子化モデルとして配備できた。
- GGUFは一般にGGML Unified Fileの略で、モデルの重み、構造、トークナイザーなどを単一ファイルへまとめる形式である。
- 使用中のMLX-LM版はQwen2の直接GGUF出力に対応していなかったため、ツールごとの役割を分けて配備した。

## 今日出てきた重要用語

- 上位互換：元のモデルの長所を維持しながら、能力が全般的に改善した状態。今回のtuned Qwenはこれには当てはまらなかった。
- FTの波及：学習させた形式や表現の癖が、学習対象とは異なる質問の回答にも現れること。
- 代表ケース評価：全件を同じ深さで読む代わりに、結論へ影響する特徴的なケースを選んで詳しく確認する方法。
- adapter：LoRAで追加学習した差分。今回のadapterはbase modelと組み合わせて推論に使う。
- GGUF：モデルの重み、構造、トークナイザーなどをまとめ、llama.cppやOllamaなどで扱えるようにする単一ファイル形式。
- merge：base modelへLoRA adapterの差分を統合し、単独で扱えるモデルへする処理。
- q4_K_M：モデルの重みを主に4bitで表現し、容量とメモリ負荷を減らす量子化方式。

## 実行したコマンドと、その意味

```text
ls -lh eval/runs/
```

保存済みの評価ファイルとサイズを確認し、Day29で再実行が必要か判断した。

```text
grep -E '^## (Q|FT-EVAL-)' eval/runs/day27_qwen_base_ft.md eval/runs/day27_qwen_tuned_ft.md eval/runs/day27_qwen_base_general.md eval/runs/day27_qwen_tuned_general.md eval/runs/day28_tinyswallow_general.md
```

各評価ファイルにQ1〜Q10が保存されているか確認した。最初に案内された`rg`は環境に入っておらず、標準の`grep`へ切り替えた。

## 今日作成したもの

- `eval/runs/day29_final_outputs.md`：モデル別の保存出力を質問単位へ並べ直した全量版
- `eval/final_eval.md`：既存評価と代表6ケースを使った短い最終評価
- `src/build_day29_final_outputs.py`：保存済み出力を質問単位で統合するスクリプト
- `README.md`：RAG、FT、現在の配備状態、最終評価を追記
- `finetune/tuned_qwen_fused/`：base modelとadapterを統合したモデル
- `finetune/tuned_qwen_f16.gguf`：llama.cppで変換したF16 GGUF
- `finetune/Modelfile.tuned_qwen`：Ollama登録用の設定
- `finetune/day29_deployment.md`：mergeからOllama推論までの配備記録
- Ollamaモデル`tuned-qwen-day29:latest`：q4_K_M、約4.7GB

配備後、14GBの統合済みモデルと14GBのF16 GGUFは再生成可能な中間生成物として削除した。Ollama側に残った未使用のF16 blobも、manifestから参照されていないことを確認して削除した。base model、LoRA adapter、登録済みの4.7GBモデルは残している。

出力の統合、評価の整理、README更新はCodexが担当した。ユーザーは、保存ファイルの存在と件数をコマンドで確認し、最終評価の結論を自分の実感と照合した。

## まだ曖昧なこと

- 形式崩れの主因がデータ量、学習量、教師データの一貫性、トークン切り捨てのどれか
- 80、160、240 iterationのどの時点で副作用が強くなったか
- 量子化後のOllamaモデルが、MLX上の固定評価10件でも同等の傾向を示すか
- 少数の代表ケースだけで、どこまで安定してモデル品質を判断できるか

## 自分の言葉でのまとめ

せっかく学習させたので良くなってほしかったが、tuned Qwenはbase Qwenのシンプルな上位互換ではなかった。情報を保持して捏造が減った部分はある一方、指定形式を守れなかったり、学習内容が別の質問にも波及したりした。FTは単純な性能アップではなく、狙った変化と副作用を実出力で確認する必要がある。ただし、学習したモデルをGGUFへ変換し、Ollamaから実際に呼び出すところまで一周できた。
