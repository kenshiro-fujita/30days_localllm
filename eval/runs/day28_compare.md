# Day28 モデル比較メモ

## 比較条件

- 質問・素材：`eval/questions.md`、`eval/materials.md`
- TinySwallow：Day28にOllamaで実行
- base Qwen／tuned Qwen：Day27に保存した出力を再利用
- 最大生成トークン数：512
- temperature：0

## 質問別の評価

- Q1：base Qwen。ローカルLLMの説明が最も正確だった。
- Q2：tuned Qwen。RAGを正しく説明し、具体例も適切だった。
- Q3：tuned Qwen。箇条書きで読みやすく、base Qwenのような中国語混入もなかった。
- Q4：僅差でtuned Qwen。業務プロセス、自動化、人間の経験など幅広く聞けていた。
- Q5：tuned Qwen > base Qwen >> TinySwallow。tuned Qwenが簡潔に3観点を整理した。TinySwallowはモデルの訓練に寄った説明だった。
- Q6：base Qwen ≒ tuned Qwen。TinySwallowは素材にない意味を一部追加した。
- Q7：3モデルとも正答。
- Q8：TinySwallowは5営業日前という期限を拾ったが、全モデルが注意事項の一部を落とした。
- Q9：tuned Qwenが3秒以内の応答と夜間バッチ1日1回の食い違いを最も明確に扱った。ただし長くなり途中終了した。
- Q10：TinySwallowとbase Qwenは人間による最終確認を維持した。tuned Qwenは素材にない「担当者未定」を出し、FT由来の癖が現れた。

## 全体評価

- TinySwallowは読みやすく整った回答を出すが、RAGをRLHFと取り違えるなど重大な知識誤りがあった。
- base Qwenは正確な説明や素材読解で安定する場面があったが、冗長化、途中終了、中国語混入があった。
- tuned QwenはQ2〜Q5で簡潔さと方向性が改善した。一方、形式崩れや「担当者未定」という学習由来の癖が汎用回答にも現れた。
- FT後は、もっともらしい完全な捏造が減り、回答の方向性が変化した。しかし、すべての能力が一様に良くなったわけではない。

