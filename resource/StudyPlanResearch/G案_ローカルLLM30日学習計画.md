# **ローカルLLM開発およびファインチューニング習得に向けた30日間集中再トレーニング計画書**

## **1\. レガシー開発経験者におけるローカルLLM習得の技術的要衝**

過去にレガシー企業において3年弱のシステム開発経験を持つ技術者が、最新の大規模言語モデル（LLM）のローカル環境構築、応用アプリケーション実装、およびファインチューニング（微調整）技術を最短で習得するためには、モダンなAIエコシステム特有の設計思想を理解する必要がある1。従来のシステム開発が「確定的な論理ルールと構造化データ」を扱っていたのに対し、LLM開発は「確率論的な生成モデルと非構造化自然言語」を処理対象とする。この技術的パラダイムシフトを乗り越える上で、過去のエンジニア経験は、Web APIの制御、仮想環境の構築、環境変数管理といったシステムエンジニアリングの基礎体力として大いに活かされる1。  
LLMの学習において初心者が陥りやすい最大の落とし穴は、高度な抽象化フレームワーク（例えばLangChainやLlamaIndex）を初期段階から過剰に導入し、ブラックボックス化された挙動に翻弄されることである2。本再トレーニング計画では、まず「素のPythonとAPI」を用いた直接的な実装を徹底し、ローカル環境におけるモデルの物理的な制約（VRAM消費量、コンテキスト長、量子化の劣化率）を定量的に観察・評価できる「自走力」の育成を最優先する2。  
特に、ローカルLLM開発の核心は、有限のコンピューティング資源（特にグラフィックスメモリ、以下VRAM）に、いかにモデルを適合させるかという最適化問題に帰結する5。このリソース最適化の感覚を掴むため、30日間のカリキュラムでは「動くものを作る（実践）」と「挙動の定量的評価（理論）」を循環させながら進める1。

## **2\. 30日間チャレンジの定量的時間配分および日別マイルストーン**

本計画は、平日平均1時間、土日3時間の学習時間を基本設計とし、今日7月13日（月）を開発環境の事前整備に充てる「準備日」として設定している。明日7月14日（火）からの30日間を5つのフェーズに分け、学習負荷と実務スキルの獲得効率を最適化した時間割を以下の通り提示する。

### **30日間の学習フェーズ設計**

| フェーズ（週） | 期間 | 主な学習テーマ | 平日目標時間 | 土日目標時間 | 週間総学習時間 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **準備日** | 7月13日（月） | クラウド設定・ハードウェア仕様評価 | 1.0時間 | \- | 1.0時間 |
| **第1週** | 7月14日（火）〜7月19日（日） | ローカル推論エンジン構築と日本語小型モデルの選定3 | 1.0時間/日 | 3.0時間/日 | 10.0時間 |
| **第2週** | 7月20日（月）〜7月26日（日） | Python API制御、トークン計測、プロンプト制御2 | 1.0時間/日 | 3.0時間/日 | 11.0時間 |
| **第3週** | 7月27日（月）〜8月2日（日） | ゼロからのローカルRAG（検索拡張生成）システム開発4 | 1.0時間/日 | 3.0時間/日 | 11.0時間 |
| **第4週** | 8月3日（月）〜8月9日（日） | Google ColabとUnslothによる高速QLoRAチューニング6 | 1.0時間/日 | 3.0時間/日 | 11.0時間 |
| **第5週** | 8月10日（月）〜8月12日（水） | モデル統合・GGUF変換・ローカル展開・最終評価11 | 1.0時間/日 | \- | 3.0時間 |
| **合計** | **全30日間** | **内製推論、RAG、ファインチューニングの一気通貫開発** | \- | \- | **47.0時間** |

### **30日間の日別カリキュラムおよび実行タスク**

#### **準備日：7月13日（月）［学習目標：1.0時間］**

* **タスク**：Hugging Face、Google Colab（必要に応じてColab Pro+：月額約5,701円の課金検討）のアカウント作成10。ローカルPCのハードウェア仕様（GPU型番、VRAM容量、システムRAM）の把握5。

#### **第1週：7月14日（火）〜7月19日（日）［学習目標：10.0時間］**

* **7月14日（火）［1h］**：ローカルLLMを取り巻くトレンドと技術エコシステムの把握。CPU/GPUと推論メモリの関連性の理解5。  
* **7月15日（水）［1h］**：OllamaのローカルPCへのインストールと、CLIを用いた基本コマンドの動作確認（ollama run）3。  
* **7月16日（木）［1h］**：LM Studioのインストール。Hugging FaceからのGGUFモデル検索、ダウンロード、GUIチャットの実行11。  
* **7月17日（金）［1h］**：モデル量子化（Quantization）の基礎。ビット数（q4\_k\_m, q8\_0, f16等）が推論メモリ容量と回答精度、処理速度に与える影響の定量把握12。  
* **7月18日（土）［3h］**：2026年最新の日本語軽量モデルの実力検証。Qwen3-1.7B（思考モード）、Gemma 3 4B、Llama 3.2 3Bの日本語指示追従力と自然さを対話形式で定性比較8。  
* **7月19日（日）［3h］**：Ollamaにおける「Modelfile」の作成。システムプロンプトやペルソナ（口調・キャラクター設定）を注入した独自モデルのビルド方法の習得20。

#### **第2週：7月20日（月）〜7月26日（日）［学習目標：11.0時間］**

* **7月20日（月）［1h］**：Pythonによる仮想環境（venv）の構築と、ollama、requests などの必要な最小限のパッケージ導入4。  
* **7月21日（火）［1h］**：OllamaのローカルAPIエンドポイント（http://localhost:11434）に対する非構造化POSTリクエスト送信プログラムの作成22。  
* **7月22日（水）［1h］**：ストリーミング（Streaming）レスポンスの受信処理。ユーザー体験（UX）を向上させる逐次表示ロジックのPython実装24。  
* **7月23日（木）［1h］**：トークナイザー（Tokenizer）とトークン（Token）消費量の概念理解。日本語におけるマルチバイト文字のトークンカウント特性の把握6。  
* 7月24...5（金）［1h］：生成パラメータ（Temperature, Top-P, Max Tokens）の制御。生成テキストの創造性と決定論的一貫性の変化を評価5。  
* **7月25日（土）［3h］**：JSON構造化出力（Structured Outputs）の実装。LLMから一貫したスキーマデータ（例：感情分析や要約結果）を取得するパーサの実装。  
* **7月26日（日）［3h］**：第2週ミニプロジェクト。過去の対話履歴（Context Window）をインメモリで保持・管理する、コマンドライン対話チャットのPython自作。

#### **第3週：7月27日（月）〜8月2日（日）［学習目標：11.0時間］**

* **7月27日（月）［1h］**：RAG（検索拡張生成）の全体像とアーキテクチャ設計。外部データ（PDF/Markdown）をLLMが参照する仕組みの全体理解2。  
* **7月28日（火）［1h］**：テキスト埋め込み（Embedding）モデルの概念。Ollama（nomic-embed-text）を用いたベクトル化コードの実装4。  
* 7月29...4（水）［1h］：ChromaDBのインストールと、永続化クライアント（Persistent Client）を用いたベクトルデータベースの基本操作4。  
* **7月30日（木）［1h］**：日本語ドキュメントの分割（Chunking）。文字数ベースの適切なスプリッターの検証と、セマンティックな一貫性を保つチャンク分割の実装4。  
* **7月31日（金）［1h］**：ドキュメント自動読み込みとインジェストパイプラインの実装。複数ファイルをパースしてベクトルに変換し、ChromaDBに登録する流れの構築4。  
* **8月1日（土）［3h］**：RAGシステムにおけるセマンティック検索の実装。ユーザー質問ベクトルに対する類似チャンクの抽出と、LLMプロンプトへのコンテキスト注入4。  
* **8月2日（日）［3h］**：応用実装およびノーコード比較。RRF（相互ランク融合）アルゴリズムを用いたキーワード検索とベクトル検索のハイブリッド化、およびAnythingLLMやObsidianを用いたノーコードRAGとの機能検証2。

#### **第4週：8月3日（月）〜8月9日（日）［学習目標：11.0時間］**

* **8月3日（月）［1h］**：ファインチューニング（SFT）とLoRA/QLoRAの基本概念。重み行列の低ランク近似と4bit量子化によるVRAM低減メカニズムの習得5。  
* **8月4日（火）［1h］**：Google Colab Pro+等のクラウドGPU環境の準備。Unslothライブラリの依存関係と、最新バージョンの整合性確認10。  
* **8月5日（水）［1h］**：ベースモデル（Gemma 3 4B-it / Qwen 2.5等）のロード。Unslothによる4bit最適化読み込みコード（FastLanguageModel.from\_pretrained）の実装10。  
* **8月6日（木）［1h］**：チャットテンプレートの適応。ShareGPT形式およびChatML形式のデータ前処理、standardize\_sharegpt によるフォーマット標準化関数の実装10。  
* **8月7日（金）［1h］**：学習パラメータ（Learning Rate, Epoch, Batch Size, r=16, lora\_alpha=32）の設計理論。過学習（Overfitting）と学習崩壊の検知手法の習得5。  
* **8月8日（土）［3h］**：カスタム指示データセットの構築。JSONL形式による独自の専門データ（社内規定、専門用語集等）または公開データセットのクレンジング、前処理関数の実装7。  
* **8月9日（日）［3h］**：ファインチューニングの実行。SFTTrainerを用いた学習処理のトリガー、Loss（損失関数）のグラフ可視化（WandB等）と収束性の分析7。

#### **第5週：8月10日（月）〜8月12日（水）［学習目標：3.0時間］**

* **8月10日（月）［1h］**：学習モデルのマージ（Merge）およびGGUFエクスポート。Unslothの save\_pretrained\_gguf メソッドを用いた、q4\_k\_m等の任意の量子化形式への1ステップ変換処理12。  
* **8月11日（火）［1h］**：出力されたGGUFモデルのローカルPCへの配置。LM StudioやOllamaを用いたローカルデプロイ、推論サーバーのローカル起動テスト11。  
* **8月12日（水）［1h］**：テストスクリプトを用いた独自モデルの最終評価（テストデータに対する生成応答の定性チェック、RAGシステムとの結合テスト）9。30日間の進捗と完成コードをGitHub公開リポジトリに整理2。

## **3\. 推論エンジンの理解とローカル起動（第1週）**

ローカルLLM開発において最初に取り組むべきは、ローカル推論エンジンの特徴把握と適切な日本語モデルの選定である3。エンジニア経験者は通常、高スペックなクラウドインスタンスを前提にしがちだが、ローカル環境においてはハードウェアメモリ（VRAM）の制約がそのまま動作モデルの上限を規定する5。

### **2026年最新の主要日本語対応モデルのスペック比較**

| モデル名 | 開発元 | パラメータ数 | 推奨VRAM容量 (Q4\_K\_M量子化) | 日本語対応特性 | 主な特徴と注意点 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Qwen3-0.6B** | Alibaba | 6億 | 約2GB以下 | コスパの帝王。軽量で爆速8 | スマホや極限の低リソース環境でも動作。ただし、複雑な思考タスクは不得意8。 |
| **Qwen3-1.7B** | Alibaba | 17億 | 約3GB〜4GB | 非常に滑らか、ジョークまで対応8 | 1.7Bとしては驚異的な日本語表現力。思考モード（Thinking Mode）のON/OFF制御が可能8。 |
| **Gemma 3 4B** | Google | 40億 | 約6GB〜8GB | 日英翻訳性能に優れる8 | 多言語トークナイザーが大幅強化。1B版に比べ指示追従性と自然な敬語表現が大幅向上8。 |
| **Qwen3-8B** | Alibaba | 80億 | 約10GB〜12GB | 非常に流暢、専門用語も対応33 | VRAM 12GB以上のGPUが必要。推論速度、コンテキスト理解、コーディング能力のバランスに秀でる21。 |
| **Gemma 3 12B** | Google | 120億 | 約14GB以上 | 緻密な文脈処理が可能33 | 個人環境での最大実用クラス。VRAM不足時はシステムRAMへのオフロードによる超低速化に注意33。 |

推論エンジンの動作特性において、量子化技術は極めて重要な役割を果たしている5。モデルの元々の重みは32ビットや16ビットの浮動小数点（FP32/FP16）で表現されているが、これを4ビット（Q4\_K\_Mなど）に圧縮することで、モデルサイズを約4分の1に削減できる5。この量子化処理により、本来であれば動作に30GB以上のVRAMを要求する8B（80億パラメータ）モデルが、一般的なコンシューマ向けGPU（VRAM 8GB〜12GBクラス）で快活に動作するようになる6。量子化による精度の低下は、近年の量子化技術の進歩により1〜2%程度に抑えられており、個人開発においてはこのトレードオフを活用することがデファクトスタンダードとなっている10。  
Ollamaは、これらGGUF形式のモデルをDockerライクなシンプルなコンテナ構造で隠蔽し、バックエンドのGPU演算最適化を隠蔽してCLIから簡単に実行できるため、最初の検証用ツールとして極めて適している3。

## **4\. Python API連携とプロンプト制御（第2週）**

レガシーな技術要素からモダンなLLM開発へと移行する際、最も強力な武器となるのが「Pythonを用いたAPI連携の実装」である1。LLMは、テキストを入力するとテキストを返すという、本質的にはステートレス（状態を持たない）なAPIとして動作する9。

### **LangChain非依存のAPIプロトタイプの有用性**

開発コミュニティにおいて広く紹介されているLangChainやLlamaIndexなどのオーケストレーションフレームワークは、初心者に対して「過度なブラックボックス」を提供する2。例えば、APIリクエストの内部でどのようなシステムプロンプトが構築され、トークンがどのように消費されているかを監視することが、これらのフレームワークを使用すると極めて難しくなる2。  
したがって、本ロードマップでは、以下のようなPython標準の requests や公式の ollama クライアントを用いた「ベタ書きのAPI連携」を推奨する2。これにより、ネットワークエラー時のリトライ処理や、タイムアウトの最適化設計、トークナイザーの厳格な制御など、レガシーエンジニアが本来得意とする堅牢なプログラム設計手法をそのままLLM開発に持ち込むことができる2。

### **Ollama REST APIにおけるストリーミング受信とトークン消費追跡のPython実装**

Python  
import json  
import requests

def call\_local\_llm\_stream(prompt\_text: str):  
    """  
    ローカルで起動しているOllamaのREST APIを直接叩き、  
    ストリーミングレスポンスを受信して逐次表示する関数。  
    """  
    url \= "http://localhost:11434/api/generate"  
    payload \= {  
        "model": "qwen3:1.7b",  
        "prompt": prompt\_text,  
        "stream": True,  
        "options": {  
            "temperature": 0.3,  
            "top\_p": 0.85  
        }  
    }  
      
    headers \= {"Content-Type": "application/json"}  
      
    try:  
        response \= requests.post(url, data=json.dumps(payload), headers=headers, stream=True)  
        response.raise\_for\_status()  
          
        print("--- LLM Response Start \---")  
        for line in response.iter\_lines():  
            if line:  
                decoded\_line \= line.decode('utf-8')  
                json\_data \= json.loads(decoded\_line)  
                  
                \# 逐次テキストを出力  
                token\_chunk \= json\_data.get("response", "")  
                print(token\_chunk, end="", flush=True)  
                  
                \# 生成完了フラグがある場合、推論スタッツを出力  
                if json\_data.get("done", False):  
                    print("\\n--- LLM Response End \---")  
                    eval\_count \= json\_data.get("eval\_count", 0)  
                    eval\_duration \= json\_data.get("eval\_duration", 1) / 1e9  \# ナノ秒から秒へ変換  
                    print(f"消費トークン数（生成分）: {eval\_count} tokens")  
                    print(f"推論生成時間: {eval\_duration:.2f} seconds")  
                    print(f"生成速度 (Token/s): {eval\_count / eval\_duration:.2f} t/s")  
                      
    except requests.exceptions.RequestException as e:  
        print(f"\\n\[APIエラー\]: ローカルOllamaサーバーとの通信に失敗しました。{e}")

if \_\_name\_\_ \== "\_\_main\_\_":  
    call\_local\_llm\_stream("なぜローカルLLMを使用すると、企業のセキュリティポリシーに準拠しやすいのですか？詳細を日本語で回答してください。")

この実装を通じて、非同期で送られてくるネットワークパケットを逐次処理する感覚が得られる。また、Ollamaがレスポンスの最後に返すメタデータ（eval\_count, eval\_duration）を直接パースすることにより、生成速度がシステム仕様に対して実用的であるかを客観的に評価する目が養われる3。

## **5\. ゼロから構築する完全ローカルRAG（第3週）**

RAG（Retrieval-Augmented Generation：検索拡張生成）は、LLMのパラメータを書き換えることなく、最新データや非公開の独自データを安全に参照させて誤答を防止する最も実用的なシステムパターンである5。

### **ローカルRAGの機能相関とパイプライン**

ローカル環境におけるRAGパイプラインは、情報の「インジェスト（格納）」と「検索・生成（呼び出し）」の2つのフェーズに分かれ、それらは以下に示す相互関連プロセスのもとに機能する4。

【インジェストフェーズ】  
 独自ドキュメント（PDF/MD等）  
       │  
       ▼ (RecursiveCharacterTextSplitterによるチャンク分割: 500文字前後) ── \[メタデータの自動付与\]  
 チャンク化テキスト群  
       │  
       ▼ (Ollama / nomic-embed-text によるベクトル化: 768次元)  
 ベクトル埋め込みデータ  
       │  
       ▼ (ChromaDB 永続化データベースへの格納)  
 ローカルベクトルストア

【検索・生成フェーズ】  
 ユーザー質問クエリ ──► \[埋め込みモデル\] ──► 質問ベクトル  
                                            │  
                                            ▼ (ベクトル検索: コサイン類似度トップK抽出)  
                                     関連チャンクの特定  
                                            │  
                                            ▼ (ハイブリッド検索: 語彙BM25 \+ ベクトルRRF統合)  
                                     最適化コンテキスト構築  
                                            │  
                                            ▼ (LLMプロンプトへのコンテキスト注入)  
                                     LLMによる回答生成

この各プロセスは、単に組み合わせるだけでなく、各パラメータを日本語の処理特性に合わせて緻密に調整しなければ精度が著しく低下する2。

### **日本語RAGにおける定量的パラメータチューニング**

日本語ドキュメントを対象にRAGを組む場合、英語圏のチュートリアルに書かれているパラメータ設定をそのまま踏襲すると、検索漏れや文脈の断片化が発生する4。

1. **チャンクサイズ（Chunk Size）の最適化**： 英語のRAGでは一般的に1,000〜1,500トークン前後が推奨されるが、これは文字に換算すると非常に長大であり、かつ英語は語彙密度が日本語よりも低い4。日本語のドキュメント（技術書、社内規定など）を処理する場合、情報が濃縮されているため、「500文字前後（オーバラップ100文字）」がセマンティック抽出のベストプラクティスとなる4。これより大きすぎると不要な情報が混入し（ノイズ）、小さすぎると文脈の主語が欠落する（コンテキストロス）4。  
2. **タイトル埋め込み（Title Embedding）の実装**： 単にテキストを500文字でぶつ切りにすると、中間のチャンクが「何についての説明か」を示す主語（例：製品名など）を失ってしまう4。これを回避するため、分割した各チャンクの先頭に、パーサが取得したドキュメント名やヘッダー情報を自動的に付加するロジック（\[製品Aマニュアル\] ...チャンク本文...）をPythonで実装する4。これを行うだけで、ベクトル検索の検索適合率が劇的に改善される4。  
3. **ハイブリッド検索とRRF（相互ランク融合）**： ローカルで動作する軽量埋め込みモデル（例：nomic-embed-text）は、日本語の高度な意味関係の理解が苦手な場合がある4。そこで、単純な意味検索（ベクトル検索）だけでなく、特定の固有名詞やコードに完全一致するキーワード検索（BM25アルゴリズムなど）を裏側で同時に走らせる2。この両者から得られた検索結果順位を、RRF（Reciprocal Rank Fusion）と呼ばれる手法を用いて結合し、トップ ![][image1]（通常は ![][image2] 程度）のドキュメントを抽出する4。これにより、スペルミスや表記揺れに強い検索パイプラインが完成する2。

### **RAGシステムの定量的評価：Hit-RateとMRR**

RAGシステムを「構築して終わり」にしないために、検索精度の定量的評価ロジックを第3週の終わりに手動で実装する32。

* **Hit-Rate（ヒット率）**：事前に用意した「想定質問と回答の正解セット」を用いて、質問を投げた際に類似ドキュメント上位 ![][image1] 件の中に、真に参照すべきドキュメント（正解チャンク）が含まれていた確率を算出する32。  
* **MRR（Mean Reciprocal Rank：平均逆順位）**：正解ドキュメントが上位の何番目にヒットしたかを評価する指標であり、以下の数式で定義される32。

![][image3]  
ここで、![][image4] はテストクエリの総数、![][image5] は ![][image6] 番目のクエリにおいて、抽出されたドキュメントリスト内で正解チャンクが初めて現れた順位である32。もし正解ドキュメントが1位でヒットすれば逆順位は ![][image7]、3位であれば ![][image8]、ヒットしなければ ![][image9] となる32。これらHit-RateやMRRをコード上で自動算出する仕組み（ゴールドスタンダード評価セット）を作ることで、チャンクサイズや重複文字数の調整がシステム精度をどのように変動させるかを、エンジニアリングの観点から定量的に証明・最適化できるようになる2。

## **6\. Google ColabとUnslothを活用したQLoRAチューニング（第4週・第5週）**

ローカル環境におけるモデル推論やRAGの最適化をマスターした後の最終ステップは、LLMの「ファインチューニング（微調整）」である1。RAGが「外部の情報をその都度参照させる行為（カンペを見せる）」であるのに対し、ファインチューニングは「LLM自体の文体、回答スタイル、ドメイン固有の指示に対するフォーマット追従力を自律的に獲得させる行為（脳を書き換える）」である5。

### **クラウドGPUコストと効率性の担保：Colab Pro+とUnslothの優位性**

ファインチューニングを実行するためには、モデルの数億、数億万ものパラメータに対して誤差逆伝播法（Backpropagation）を適用し、勾配計算を行う必要があるため、極めて大容量のVRAMと高い演算性能が求められる5。  
個人のローカル環境（例：VRAM 8GB〜12GBのコンシューマPC）でフル学習を走らせることは不可能に近いが、Google ColabのプレミアムGPUリソース（T4、A100等）を活用することで、極めて安価に短時間でファインチューニングの実験を回すことができる6。特に、ファインチューニング実行時にOut Of Memory（OOM）による異常終了を避け、安定してバックエンド処理を回し続けるためには、Google Colab Pro+（月額約5,701円）などの有料プランを活用することが実質的な推奨アプローチとなる14。  
学習用ライブラリとして定番である「Unsloth」は、GPU専用のカスタムカーネルを手書き（Triton言語等）で記述し、メモリのオーバーヘッドを劇的に排除することで、学習速度を2〜5倍高速化し、VRAM消費量を50%〜80%削減するオープンソースソフトウェアである7。これにより、通常であればエンタープライズ向けの数百万クラスのGPUマシンを必要としたGemma 3 4Bや12B、あるいはQwen3-8Bなどのクラスのモデルが、Colabの無料枠から有料枠の範囲内で、ものの数十分から数時間で学習完了可能となる7。

### **データセットの標準化とフォーマット処理：standardize\_sharegpt**

ファインチューニングの成否は、与える学習データの「品質」と「フォーマットの厳格さ」に100%依存する26。モデルは、インプットとアウトプットが特定の特殊な記号（特殊トークン）で区切られたテンプレート形式（ChatMLやAlpacaなど）を前提として調整されているため、生のテキストデータをそのまま与えても正常に学習できない12。  
Unslothを用いる場合、インターネット上に点在する様々な形式（ShareGPT、Alpaca、カスタム会話ペア等）のデータフォーマットを、モデルが本来要求する入力構造に簡単かつ一元的に揃えるためのヘルパー関数群（standardize\_sharegpt 等）が提供されている10。

#### **Hugging Faceデータの読み込みとShareGPTフォーマットへの適合処理**

Python  
from datasets import load\_dataset  
from unsloth import standardize\_sharegpt

def prepare\_training\_dataset(tokenizer, dataset\_name="mlabonne/FineTome-100k"):  
    """  
    データセットをロードし、ShareGPTの共通会話フォーマット(role/content)に標準化し、  
    特定のチャットテンプレートを適用するデータ前処理パイプライン関数。  
    """  
    \# 1\. データセットのロード  
    dataset \= load\_dataset(dataset\_name, split="train\[:5000\]")  \# 高速実験のため最初の5000件を使用 \[cite: 2, 29\]  
      
    \# 2\. フォーマットを標準の role / content スキーマへ変換  
    dataset \= standardize\_sharegpt(dataset)  
      
    \# 3\. チャットテンプレート適用関数の定義  
    def apply\_chat\_template\_format(examples):  
        conversations \= examples\["conversations"\]  
        \# 各サンプルに対してモデルのトークナイザー専用チャットテンプレート（例：Gemma 3やQwen用）を適用  
        formatted\_texts \= \[  
            tokenizer.apply\_chat\_template(convo, tokenize=False, add\_generation\_prompt=False)  
            for convo in conversations  
        \]  
        return {"text": formatted\_texts}  
      
    \# 4\. マッピング処理によるデータ変換の実行  
    dataset \= dataset.map(apply\_chat\_template\_format, batched=True)  
    return dataset

この前処理を施したデータを用いてファインチューニングを行うことで、モデルの内部表現が破壊される「壊滅的忘却」を防ぎ、本来持っている汎用能力を維持したまま、ターゲットとする業務タスクや文体スタイルを高精度で獲得させることが可能になる5。

### **学習データの品質向上と可観測性：Unsloth StudioとData Recipes**

ファインチューニングをさらに効率化し、コード不要でデータセットを合成・クレンジングするアプローチとして、近年導入された「Unsloth Studio」のデータ成形ワークフロー「Data Recipes（データ・レシピ）」がある5。  
これは、PDF、CSV、JSONなどの非構造化ドキュメントをアップロードするだけで、グラフノード型の可視化エディタ（ワークフロー）上で視覚的にデータを結合・合成し、LLMファインチューニング用の美しい指示データセット（合成データセット）へと自動変換するノーコード・ローコード基盤である5。学習者は、コードによるデータクレンジングに疲弊することなく、「プロンプト」「Structured Output」「データの合成ブロック」をキャンバス上でつなぎ合わせ、バグのあるデータを早期にプレビュー確認（検証機能）で排除して、モデルに適合した最高精度のカスタムデータセットを生成できる37。

### **最終成果物のエクスポート、量子化（GGUF）、およびローカル統合**

Google Colabの学習で得られたファインチューニング済みモデル（LoRAアダプタ）は、そのままではPython環境のコードの外（Ollama等）で動かすことができない11。これを自身のローカルPCにシームレスにデプロイし、最終週でRAGなどと結合させるために、モデルの「マージ・量子化・エクスポート」を行う11。  
Unslothは、学習したアダプタのウェイトとオリジナルのモデルを結合し、ローカル推論エンジンのデファクトである「GGUF」ファイルとして1ステップで書き出す機能をネイティブでサポートしている12。

#### **GGUF直接書き出し、Hugging Face直接保存**

Python  
\# ファインチューニング済みのモデルをマージし、4bit量子化（Q4\_K\_M形式）の単一GGUFファイルとしてエクスポート  
model.save\_pretrained\_gguf(  
    "my\_local\_finetuned\_model",   
    tokenizer,   
    quantization\_method="q4\_k\_m"  
)

\# もしくは、作成したGGUFモデルをHugging Face Hubの自身のリポジトリに直接自動プッシュして共有  
model.push\_to\_hub\_gguf(  
    "your\_hf\_username/my\_local\_finetuned\_model",  
    tokenizer,  
    quantization\_method="q4\_k\_m"  
)

この処理により生成された my\_local\_finetuned\_model-unsloth.Q4\_K\_M.gguf ファイルをローカルPCにダウンロードし、LM StudioやOllamaの所定のディレクトリに配置・インポートすることで、学習した「専門的な知識や独自の口調」を完全に再現するモデルを、手元でインターネット接続を一切遮断した「100%機密保持環境（ローカル）」で、何度でもコストフリーで実行することが実現する13。

## **7\. 総括**

本計画は、レガシーエンジニアのバックグラウンドを持つ者が、最先端のローカルLLM技術スタックを確実に掌握し、一過性の「ツール利用ユーザー」から「内製開発・微調整が可能な自走力のある開発者」へと昇華するための実践に裏付けられた実効的な再トレーニング計画である1。  
30日間の学習を進めるにあたり、最終的な目標は単に「動いた」という自己満足に留めず、自作したコードやパラメータ調整の検証履歴、Hit-Rate等の評価結果データをすべてGitHubの公開リポジトリ（Public Repository）として整理・発信することである2。この「どのような技術仕様に基づいて設計を選択し、それをいかに客観的に計測・評価したか」が README.md 上に論理的に記述されたポートフォリオは、レガシー領域からモダンAI開発領域へのスキルの完全な転換を客観的に証明する、最大の技術的証跡となる2。  
今日7月13日の基本環境整備、そして明日7月14日からの1日1時間（土日3時間）の徹底的な実践トレーニングにより、最新のオープンソースLLMを思い通りにチューニングし操る能力の習得が可能となる1。

#### **引用文献**

1. LLMの難易度を徹底解説！学習ロードマップと必須スキル \- 株式会社アイティークロス, [https://www.itcross.jp/media/274/](https://www.itcross.jp/media/274/)  
2. LLMエンジニアの学習ロードマップ2026｜実務で使える生成AIスキルを6ヶ月で身につける順序, [https://it-careerlab.com/articles/llm-engineer-learning-roadmap](https://it-careerlab.com/articles/llm-engineer-learning-roadmap)  
3. OllamaでローカルにLlama 3.2を展開するステップバイステップガイド \- Apidog, [https://apidog.com/jp/blog/how-to-run-llama-3-2-locally-using-ollama/](https://apidog.com/jp/blog/how-to-run-llama-3-2-locally-using-ollama/)  
4. RTX 4080でRAGを自作する — Ollama × ChromaDB × Python 150行の全記録 \- Zenn, [https://zenn.dev/seeda\_yuto/articles/local-rag-ollama-chromadb](https://zenn.dev/seeda_yuto/articles/local-rag-ollama-chromadb)  
5. LLM ファインチューニングガイド | Unsloth Documentation, [https://unsloth.ai/docs/jp/meru/fine-tuning-llms-guide](https://unsloth.ai/docs/jp/meru/fine-tuning-llms-guide)  
6. ローカルLLMでファインチューニング \- Speaker Deck, [https://speakerdeck.com/knishioka/rokarullmdehuaintiyuningu](https://speakerdeck.com/knishioka/rokarullmdehuaintiyuningu)  
7. 【Llama3】Unslothで爆速ファインチューニング(QLoRA) | EdgeHUB \- HIGHRESO, [https://highreso.jp/edgehub/machinelearning/llama3unsloth.html](https://highreso.jp/edgehub/machinelearning/llama3unsloth.html)  
8. 2026年最新！小型LLM日本語ガチランキング【Qwen3 vs Gemma3 vs TinyLlama】Ollamaで爆速カスタム術も \- Zenn, [https://zenn.dev/kewa8579/articles/2996512cafaec4](https://zenn.dev/kewa8579/articles/2996512cafaec4)  
9. Build a Local RAG Chatbot with Ollama and ChromaDB: No Cloud Required (2026), [https://use-apify.com/blog/local-rag-chatbot-ollama-chromadb-tutorial](https://use-apify.com/blog/local-rag-chatbot-ollama-chromadb-tutorial)  
10. Google ColabとUnslothを使ってLlama 3 (8B)をファインチューニングし、Ollamaにデプロイする方法 \- Zenn, [https://zenn.dev/sunwood\_ai\_labs/articles/fine-tune-llama-3-8b-with-google-colab-and-unslo](https://zenn.dev/sunwood_ai_labs/articles/fine-tune-llama-3-8b-with-google-colab-and-unslo)  
11. Unslothを使ってIBM Granite 4.0を自作の日本語データセットでファインチューニングした話 \- Qiita, [https://qiita.com/kolinz/items/085d5b4dd62af931b6e4](https://qiita.com/kolinz/items/085d5b4dd62af931b6e4)  
12. UnslothでLlama3をファインチューニングする \- Zenn, [https://zenn.dev/the\_exile/articles/unsloth-llama3-fine-tuning](https://zenn.dev/the_exile/articles/unsloth-llama3-fine-tuning)  
13. GGUF に保存 | Unsloth Documentation, [https://unsloth.ai/docs/jp/ji-ben/inference-and-deployment/saving-to-gguf](https://unsloth.ai/docs/jp/ji-ben/inference-and-deployment/saving-to-gguf)  
14. 手元で動く軽量の大規模言語モデルを日本語でファインチューニングしてみました(Alpaca-LoRA)｜masa\_kazama \- note, [https://note.com/masa\_kazama/n/nabaa6dfec741](https://note.com/masa_kazama/n/nabaa6dfec741)  
15. Fine-tuning Gemma 3 on a Custom Web Dataset With Firecrawl and Unsloth AI, [https://www.firecrawl.dev/blog/gemma-3-fine-tuning-firecrawl-unsloth](https://www.firecrawl.dev/blog/gemma-3-fine-tuning-firecrawl-unsloth)  
16. Unsloth Studio Fine-Tuning LLMs Guide \- DataCamp, [https://www.datacamp.com/tutorial/unsloth-studio-fine-tuning-llms-guide](https://www.datacamp.com/tutorial/unsloth-studio-fine-tuning-llms-guide)  
17. ローカルLLMをWindows PCで触ってみる：OllamaとOpen WebUIで始める入門手順, [https://cloud5.jp/saito-how-to-get-started-with-a-local-llm/](https://cloud5.jp/saito-how-to-get-started-with-a-local-llm/)  
18. How to Build a RAG Solution with Llama Index, ChromaDB, and Ollama \- DEV Community, [https://dev.to/sophyia/how-to-build-a-rag-solution-with-llama-index-chromadb-and-ollama-20lb](https://dev.to/sophyia/how-to-build-a-rag-solution-with-llama-index-chromadb-and-ollama-20lb)  
19. 非力なPCでもAIは加速する、ローカルLLM「Gemma」と「NVIDIA Nemotron」の二刀流運用ロードマップ【ローカルAI】 \- ドモドモコーポレーション, [https://www.dm2.co.jp/blog/38230](https://www.dm2.co.jp/blog/38230)  
20. 2026年最新 | OllamaでGemma 3を動かす完全ガイド：日本語性能から推奨スペック、導入手順まで徹底解説 \- Saiteki AI, [https://saiteki-ai.com/basics/ai-tool/ollama/ollama-gemma/](https://saiteki-ai.com/basics/ai-tool/ollama/ollama-gemma/)  
21. OllamaでQwen3/2.5を動かす！日本語最強ローカルLLMの導入手順とVRAM要件を徹底解説【2026年最新】 \- Saiteki AI, [https://saiteki-ai.com/basics/ai-tool/ollama/ollama-qwen/](https://saiteki-ai.com/basics/ai-tool/ollama/ollama-qwen/)  
22. Llama 3.2をローカル環境(macOS)で実行してみる：完全ガイド \#Docker \- Qiita, [https://qiita.com/YUK\_KND/items/0bde3d3d62c4979f4f0d](https://qiita.com/YUK_KND/items/0bde3d3d62c4979f4f0d)  
23. Building a Local RAG Pipeline with Python, Ollama, ChromaDB and Streamlit \- Medium, [https://medium.com/@nchinling/building-a-local-rag-pipeline-with-python-ollama-chromadb-and-streamlit-101536f02af3](https://medium.com/@nchinling/building-a-local-rag-pipeline-with-python-ollama-chromadb-and-streamlit-101536f02af3)  
24. ChromaDB \+ Ollama で作る高機能ローカルRAGシステム \#Python \- Qiita, [https://qiita.com/ishikawamasahito3150/items/c3385400dedf5ef7c515](https://qiita.com/ishikawamasahito3150/items/c3385400dedf5ef7c515)  
25. 【2026年最新】LLM学習ロードマップが激変！今から始める人への完全ガイド \- Note, [https://note.com/kojima\_product/n/n4ca373548148](https://note.com/kojima_product/n/n4ca373548148)  
26. Comprehensive Guide to Preparing Data for Fine-Tuning Models with Unsloth \- Ithy, [https://ithy.com/article/data-preparation-fine-tuning-n7sxu2w4](https://ithy.com/article/data-preparation-fine-tuning-n7sxu2w4)  
27. 【構想・設計準備】自身の思考回路を学習させたローカルLLMの個人構築、AIデジタルツイン（分身）の作成ってもしかしてできそう？【戦略枠組み仮置き】｜KATHMI / 吉田佳寿美 \- note, [https://note.com/kathmi/n/n637d7b42d435](https://note.com/kathmi/n/n637d7b42d435)  
28. Unslothによるファインチューニングについて \- AI実装検定, [https://kentei.ai/blog/archives/1977](https://kentei.ai/blog/archives/1977)  
29. Datasets Guide | Unsloth Documentation, [https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide)  
30. 日本語LLMのファインチューニング入門 – 自作・Hugging Face公開データセット対応, [https://child-programmer.com/llm-ft-tutorial/](https://child-programmer.com/llm-ft-tutorial/)  
31. ローカルLLM ファインチューニング入門 — LoRA/QLoRA/Unsloth \- Qiita, [https://qiita.com/y0kud4/items/17b9ebbffa29278bd3dd](https://qiita.com/y0kud4/items/17b9ebbffa29278bd3dd)  
32. Fully Local RAG Pipeline with Chroma \+ Ollama | Developer Documentation \- LlamaParse, [https://developers.llamaindex.ai/python/examples/cookbooks/local\_rag\_with\_chroma\_and\_ollama/](https://developers.llamaindex.ai/python/examples/cookbooks/local_rag_with_chroma_and_ollama/)  
33. 日本語対応 LLM model の個人的評価 \- 真夜中の歌声, [https://www.mayonakanouta.com/blog/llm-models-tested](https://www.mayonakanouta.com/blog/llm-models-tested)  
34. OllamaでGoogleのLLM、Gemma 3を試す \- CLOVER \- はてなブログ, [https://kazuhira-r.hatenablog.com/entry/2025/03/16/002801](https://kazuhira-r.hatenablog.com/entry/2025/03/16/002801)  
35. Liquid LFM2.5：実行とファインチューニング | Unsloth Documentation, [https://unsloth.ai/docs/jp/moderu/tutorials/lfm2.5](https://unsloth.ai/docs/jp/moderu/tutorials/lfm2.5)  
36. Unsloth \- Train and Run Models Locally, [https://unsloth.ai/](https://unsloth.ai/)  
37. Unsloth Data Recipes, [https://unsloth.ai/docs/new/studio/data-recipe](https://unsloth.ai/docs/new/studio/data-recipe)  
38. Ollama(Qwen3-VL)×Playwrightで作る完全無料のWeb調査エージェント \- Zenn, [https://zenn.dev/lluminai\_tech/articles/358bee9674ed4e](https://zenn.dev/lluminai_tech/articles/358bee9674ed4e)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAAA1UlEQVR4XmNgGAWDCswG4k9A/B8Jv0JRwcDwBUkOhL1RpTEBTCE20ATE59EFcQFGBohBt9AlgOAyEPuiC+ID2QwQw8KRxJiA+B8QcyGJEQVeMqB60RCInyLxSQLI4TUNyj6GkCYNgDRfYIC4UAvKxxUZeAEsvP4giS2BiuUjiREFXjNgdwVZrsOl6S0DRFwRXQIXYGaAaDiNLgEEqgwQuffoErhAPwNEQyi6BBTAXC2ILoEMljFA8uM7KP7KAEmgMCDDAHERKK09ZoCovYckPwpGAV0BAEyiPUPBX4WpAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAaCAYAAAANIPQdAAABgklEQVR4Xu2WPS8FQRSGX0SERKHSSESh0Un4ARKdKMWPUFCpRXkbncJnfMRP0IhWoyDRKZCIAkEiROL7nJwZzh672bn3xt0t5kne5M77nt2cndnZuUAkEokUzDLpkfSldJOoAJ5UxhpLxg3hlTRD6ia1k0ZJF7ogBP8AacyTjqzZYPQke40kKnJoglx0agPihDRuzQLg/uZIK6TJZBTGFOQm+uJm0iepQ3lFkvWWBXON5E0GSVdqXAbqfki9Hxfd74PfuBRwT3uQyd91Y/4IBcMXHENWdMCNa525TtJWhjZJG6R10hpkf/HXPQTup1eNZ50XhN+P78rbdt608soI97hvzTRukT4j9azmf9BqDVTRY1bhHcTvs0EObaRKlcpjFdLLsPHZezPeH1oghYc2IPoh2YMNCoD38gfkPPfw3uf+lpSXygKkcMIGDr/KXTZoMHxmvxjvHOlv4A87kP+r907PkIPf0wNZQf5cX0Jqz1ReBEOQh/JnOvcViUQikUikBr4BantwVZMZtuwAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAAA3klEQVR4XmNgGAWDCswD4s9A/B+KF6DIQsBfBoQ8CDujSmMCZMXYwD4gVkEXxAYYgXg7EK9ngBgWhCoNBrgswQD5QGwCZeNy3R90AVzgLRL7AwPEMD4kMTUg7kTi4wXILgGFC4h/E0lsGRDzIPFxAlB4bUYTQ/cqNm9jBcjhhSwGMqAbyv+FJIcXvEMXgAKY67SBuAVNDifA5YXdDBC5e0DMiSaHFbAA8V50QShgYsAMO5yAGYjfAPFJdAkk8A2If6ALooNVQPyRAZK+QOkKlPewAX0gzkYXHAWjgN4AAOakNN681zOcAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAABC0lEQVR4Xu2UP0uCURjFjwg6tYg4B60Ngd9AWqW17+IXMGhsyam5z9Bqg0suKg1FOLhFioKo/TuX533jerzCtVwSf/ADOec+j3p9EdizM1zSEf1KnNJXuvCyw/Twb0iXKHew/EiLWNxwU0NSgXUdLWI4hw2fakEasO5G8ii6CF+DY90VRREaPqHv9EXyjXBL3ZPQom06S7K8f2hT0vt1P5JPL8lDFGlfQ+UR4QV1WF7SApaVNVRC9+uYwPKMFrG44XsNsf4Nn+inhkoNNlzVAquL3eszmqVzWvC6H67omL7BnoYh/Vg6ARzDlg1g/x8HXhf6Jn/mgl5ruA3ST/u8lG6BW/pAc1rs+cd8A0aqRxwVOOrxAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAaCAYAAAB7GkaWAAAAZ0lEQVR4XmNgGORAAYjvowvCwFsg/o8uSBnoBOIEdEEQ+AGlQfY5IkvMBGImKBsk6Yokx1ALpfsZ8LgUJHEBXRAERBggkmLoEiBwngFhZDkQSyPJgSV2QNmvkCVAwJkBouAPusRIAABQ1hQuO9PtsQAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEUAAAAZCAYAAABnweOlAAABb0lEQVR4Xu2WQStEURTHT1lYyUap2VohQvYWspHPYGGHiGLpC0xWtkRYWPgUyl4+gihhJysJ53TfzX3/3nvmOu5cufdX/6b5nzmv37vTNI8ok8lEZgiL1BnjLGP539giv5u8x8LhlDOMZUS8fM44r5yPIivlcSPP8P6S805f1xopj7vOr/j4HMoSZxbLgilSSARA5eNzKPIN1KGSCIDKx+dQrrFwUEkEQOXT6aHscVpYOqgkAqDykcVVLCuQzzVhJUZxUEMfmX+HqpxwjjlHnEPOAWffrHWMr08JWVzDEugnI9uElZDnmL+AykcW17EELjg9WAJWYhwHkVD5yOIGlsB3Px3BSkzgoIZeTtszPvj6lJDFTSwdpjnbWFZgJSZxEIkf+wyQWdzFgcMDFjXMk7nWAg4i4e1zznni3HFui1e5eXn0R16wAB7J7LrXku7G/VAXCe6zyJnDMnXesMgQXWGROjucQSxTZwaLTCZtPgFhoWgqVjaJmgAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAAAZCAYAAABXTfKEAAADR0lEQVR4Xu2YSchOURjHH0PIkCFDkXxiwcIQyphvgZIyxM5CIvnMQ2yILOxImVaSBaEokoikWCFDSuxsKGRYmGfO33OP77n/znvveb98t9T51dN9z/95zr3nPveMr0gikUj8lwxhIVENI5ytYDHRMjZJfcl8xoJjgbPPzn45O++sbd5dOUOd3RRtzxXylbFftN4PZ7vI5xnl7LVo3A1nPfLuYk44+ypaGbYy7y7kLZVPOltqyg9F79nZaFXSKPp8z2gqF/HJWYMp+/xYmpztM+VjojFjjBZNPclf4mwaadxA9AqUQyOkCvBsHsnoaOihRXQQrfvOaGcybbnR+H1raVHUk/yfLDi+SV4fL3rPO0YrY5KzLiy2gL6iz8bVcjnTy0DMLVO+mGmzjfY00yyVJP8+CwH8i/ZjR4DVorHvsytscC6imW0sBNgu4SQckbBeRkxSt4jGzGJHDLHJxzzXn0UCwx33W8iOGjygckfRYY91o53RO0l41DFnJZysgxLWizgnWqc7OwzzRGP2siMWVF7FYoCyxu8R3emgFw8jX4hFLBjmSnOv89Y+FxHmuoTbieRAH8COABNEdzyPnN0VXQtC7HZ2SnRXxOtgNGjUGhYJfP2jLNZguug9N7OjAo5LOPkHJP4DWq6K1uvNDgM+KGLQ8eoGFdeySFyT/DRQhu+tMWDq8fEbyWeZykKAWnP+YQnrZYyVuHeJiQmCSutZJGrdGCMCvmWk+8a0IZ1BzMzsd1dntzOtz9+IZp6wEGCyaP2W7Haw7iGmG+mcWEwzh0wZ+JgppJeCShtYNIyT2lOIPw1+JJ0bHAJza08WRQ9n2L5+cTbH2WLR03PMpgDgufNJwzr0hrStVPZt3mE0nJTtu+AkH3o3r9UzO/yZy1AJi0ctXrBgQG/lhuC0Cw1TQBFl08hEZ5dEF1EkIRb08u+mjNGH9jQYDSMdmn23dc6emzLwU+Igo6GMXZlnZKZdMFohWKVfih4YMJxxRUNwEmTQa4rwD0dvxfEcv2N2T60JziMfnJ0WbQ82AcxjZ8NJ2ykaj9zgiu3twFyESK9Mh/9VdsVW9p+D7eAMFhPVYIdvomLusZCoBvyXEvP/TKIVaGQhkUgk6uc3FC7mLqUovlYAAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAZCAYAAAAv3j5gAAABN0lEQVR4Xu2UvyuFcRTGH0qSjYGy3c0iWaSk5B9ArkWyySiZ2Exm/4NkU8pg8A+wKMpys4kyWBSDH+fc77nu93087x2Mej/1dDufc97T7b6nC1RUCPot55Yvy6Wlq9juyKzlDunZQ+oVGEEa6ot6MOrun4lytiyfWb2B9Kzk1XJM7sryRk7hS0eF2yfXxBvL5HbCd2IeeuYdws+EnCa/Fn6AfM4FxELjHsJvhpwgXw8/ST7nBWKhcQvh90KOkV8Iv0I+x/u/FhrXEH495Dj5pfBz5HMeIBYaNxC+9Y6myK+G99Mvo+wdNSB8b8i/XN0u9Iy8OsflAbmz8Dl+IEPkfIYv090puSbq23u9mNX+l+SO5x6RzrnFMNJMT+YKHFk+4tMH/eyZE8s2S+PZ8oT2r1Artisq/jXfzLZVeLJTC2oAAAAASUVORK5CYII=>