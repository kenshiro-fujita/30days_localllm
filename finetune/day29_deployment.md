# Day29 tuned Qwen配備結果

## 目的

MLX LoRAで作成したQwenのadapterをbase modelへ統合し、GGUFへ変換してOllamaから利用できる状態にする。

## 配備の流れ

```text
models/RLT-7B-4bit + finetune/tuned_adapter_v1
    ↓ MLX-LM fuse --dequantize
finetune/tuned_qwen_fused（約14GB）
    ↓ llama.cpp convert_hf_to_gguf.py
finetune/tuned_qwen_f16.gguf（約15.2GB）
    ↓ ollama create -q q4_K_M
tuned-qwen-day29:latest（約4.7GB）
```

MLX-LMに付属するGGUF出力は、使用中の版では`llama`、`mixtral`、`mistral`だけに限定されており、`qwen2`へ対応していなかった。そのため、adapterの統合はMLX-LM、GGUF変換はllama.cpp、量子化と登録はOllamaに分けた。

## Ollama登録

`finetune/Modelfile.tuned_qwen`から、次の名前で登録した。

```text
tuned-qwen-day29:latest
```

量子化方式は`q4_K_M`、Ollama上の表示サイズは4.7GBだった。

## スモークテスト

会議メモを「要点」「決定事項」「次の行動」の3区分で整理させた結果、Ollama上でも3区分、数値、担当者、期限を保持した回答を生成できた。

この結果は配備と推論の疎通確認であり、量子化後の品質がMLX上の評価と同等であることを証明するものではない。厳密に比較する場合は、固定評価問題を同じ生成条件で再実行する必要がある。

## 結論

MLX上のbase modelとLoRA adapterを、Ollamaから呼び出せる4bit GGUFモデルとして配備できた。Day29の任意タスクであるadapter merge、GGUF変換、Ollama配備まで完了した。

## 配備後のクリーンアップ

Ollama登録後、再生成可能な`finetune/tuned_qwen_fused/`と`finetune/tuned_qwen_f16.gguf`は削除した。Ollamaのmanifestから参照されていなかったF16 blobも削除した。

手元には再生成元のbase model、LoRA adapter、変換手順、Ollamaへ登録した4.7GBの量子化モデルを残している。登録済みモデルは引き続き`ollama run tuned-qwen-day29`で利用できる。
