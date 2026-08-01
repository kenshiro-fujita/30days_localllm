# Day 12 学習メモ

## 今日のテーマ

TinySwallowの回答をJSON形式で受け取り、Pythonで解析・検証する構造化出力を試す。

## 今日理解したこと

### JSON文字列とPythonの辞書は別のもの

APIから返るJSONは、最初は文字列として扱われる。`json.loads()` を使うとPythonの辞書へ変換でき、`result["category"]` のようにキーを指定して値を取り出せる。

Pythonが辞書を表示すると文字列がシングルクォートになることがあるが、JSONではキーと文字列をダブルクォートで囲む必要がある。

### JSONの解析失敗

値の引用符がないJSONを `json.loads()` へ渡すと、`json.JSONDecodeError` が発生した。

TinySwallowへプロンプトだけでJSON出力を指示したときは、次のような失敗が発生した。

- JSONオブジェクトを2つ続けて出力した
- JSONをMarkdownのコードブロックで囲んだ
- JSONの後ろに説明文を追加した
- 許可していない分類名を出力した

JSONの前後に別の文章があると、出力全体をそのまま `json.loads()` で解析できない。

### プロンプトによる指定とAPIによる形式制約

system promptへ「JSONだけを出力する」「Markdownを使わない」「説明を書かない」と詳しく指定し、`temperature=0` にしても、TinySwallowは指示に反する形式を出すことがあった。

`response_format={"type": "json_object"}` を追加すると、今回の実験では純粋なJSONオブジェクトが安定して返るようになった。

プロンプトはモデルへの指示であり、必ず守られる保証ではない。API側の出力形式指定は、JSON形式を保つためのより強い制約になる。

### JSONとして正しいことと、回答内容が正しいことは別

JSONとして正しいかどうかは、LLM出力の形式の問題であり、Pythonで解析できるかを確認できる。

分類内容が正しいかどうかは、LLMの回答内容の問題である。`response_format` でJSON形式を保てても、分類判断の正しさまでは保証されない。

実験では、肯定的な感想文に対してTinySwallowが `"category": "質問"` と出力した。JSONとしては正しいが、意味上の分類は不自然だった。

### 解析後にも値の検証が必要

JSONの解析に成功しても、想定した値とは限らない。実験では、許可した4分類にない `質問・依頼` が出力された。

そこで、Python側で許可する分類と感情を集合として定義し、出力値が含まれているか検証した。

```python
allowed_categories = {"質問", "依頼", "感想", "その他"}
allowed_sentiments = {"肯定的", "否定的", "中立"}
```

形式の解析、必要なキーの存在、値の範囲、意味上の正しさを分けて確認する必要がある。

## 今日出てきた重要用語

- JSON: キーと値の組でデータを表現する形式
- 構造化出力: 決められた項目や形式でモデルの回答を受け取ること
- `json.loads()`: JSON文字列をPythonのデータへ変換する関数
- `JSONDecodeError`: JSON文字列を正しく解析できないときの例外
- `response_format`: APIの回答形式を指定する設定
- バリデーション: データの形式や値が想定どおりか検証すること
- system prompt: モデルの役割や回答ルールを指定するメッセージ

## 実行したコマンドと、その意味

```bash
python -c 'import json; text = "{\"category\": \"質問\", \"sentiment\": \"中立\"}"; result = json.loads(text); print(result); print(result["category"])'
```

正しいJSON文字列をPythonの辞書へ変換し、キーを使って値を取得できることを確認した。

```bash
python -c 'import json; text = "{\"category\": 質問}"; result = json.loads(text); print(result)'
```

不正なJSONを解析すると `JSONDecodeError` が発生することを確認した。

```bash
ollama list
```

Ollamaで利用できるモデルを一覧表示し、TinySwallowが取得済みであることを確認した。

```bash
python src/json_classifier.py
```

文章分類・要約・感情分類を行い、TinySwallowの生出力とPythonでの解析・検証結果を確認した。

```bash
nl -ba src/json_classifier.py | sed -n '1,65p'
```

Pythonファイルを行番号付きで表示し、辞書を二重の波括弧で囲んだ箇所を特定した。

## まだ曖昧なこと

- 小型モデルで分類精度を上げるために、プロンプト例をどの程度増やすと効果があるか
- JSON Schemaのような、項目や候補値まで制約する方法
- 同じ評価用文章を複数回実行した場合の分類結果の安定性

## 自分の言葉でのまとめ

JSONとして正しいのは、Pythonの文章やLLMの出力形式の話です。分類内容が正しいかは、LLMの回答内容の問題です。
