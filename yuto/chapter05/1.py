# ch05_40.py
import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv
from huggingface_hub import login

# .envファイルから環境変数を読み込む
load_dotenv()

# HuggingFace APIキーを環境変数から取得
api_key = os.getenv("HUGGINGFACE_API_KEY")

# APIキーが取得できたか確認
if not api_key:
    print("エラー: HuggingFaceのAPIキーが見つかりません。.envファイルを確認してください。")
    sys.exit(1)

# ログイン実行
try:
    login(token=api_key)
    print("HuggingFaceへのログインに成功しました")
except Exception as e:
    print(f"エラー: ログインに失敗しました: {str(e)}")
    sys.exit(1)

def zero_shot_inference():
    """問題40のzero-shot推論を実行する"""
    try:
        print("モデルをロードしています...")
        # 正しいモデル識別子を使用
        model_name = "meta-llama/Meta-Llama-3-8B"  
        
        # トークナイザーのロード
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=api_key
        )
        
        # メモリが足りない場合は量子化のための設定
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=False,
        )
        
        # モデルのロード
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=api_key,
            device_map="auto",
            quantization_config=bnb_config,
            torch_dtype=torch.bfloat16,
        )
        
        # プロンプトの準備
        prompt = """
以下の問題に答えてください。歴史的な事実をもとに、年代順に正しく並べてください。

9世紀に活躍した人物に関係するできごとについて述べた次のア～ウを年代の古い順に正しく並べよ。

ア　藤原時平は，策謀を用いて菅原道真を政界から追放した。
イ　嵯峨天皇は，藤原冬嗣らを蔵人頭に任命した。
ウ　藤原良房は，承和の変後，藤原氏の中での北家の優位を確立した。

解答:
        """
        
        print("プロンプト:", prompt)
        
        # モデル入力の準備
        model_input = tokenizer(
            prompt, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            return_attention_mask=True
        ).to(model.device)
        
        input_ids = model_input["input_ids"]
        attention_mask = model_input["attention_mask"]
        
        print("推論を実行中...")
        
        # テキスト生成
        with torch.no_grad():
            outputs = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=150,
                do_sample=False,
                temperature=0.1
            )
            
            response = outputs[0][input_ids.shape[-1]:]
            output = tokenizer.decode(response, skip_special_tokens=True)
            
            # 結果を表示
            print("\n-----生成結果-----")
            print(output)
            
            # 結果が空の場合は終了
            if not output.strip():
                print("\n警告: 生成された出力が空です。モデルが適切な回答を生成できませんでした。")
                print("エラーが発生しました。終了します。")
                sys.exit(1)
            
            # 結果をファイルに保存
            with open("zero_shot_result.txt", "w", encoding="utf-8") as f:
                f.write(f"問題:\n{prompt}\n\n解答:\n{output}")
                
            print("\nファイル 'zero_shot_result.txt' に結果を保存しました。")
            
        # メモリの解放
        del model
        del tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
    except Exception as e:
        print(f"エラー: モデル推論中にエラーが発生しました: {str(e)}")
        print(f"例外の詳細: {type(e).__name__}: {str(e)}")
        print("エラーが発生しました。終了します。")
        sys.exit(1)

if __name__ == "__main__":
    print("問題40のzero-shot推論を実行します...")
    try:
        zero_shot_inference()
    except Exception as e:
        print(f"エラー: 予期しない例外が発生しました: {str(e)}")
        print("エラーが発生しました。終了します。")
        sys.exit(1)
    
    print("完了")