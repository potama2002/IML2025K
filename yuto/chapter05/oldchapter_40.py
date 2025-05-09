import torch
from transformers import AutoTokenizer
import os
from dotenv import load_dotenv

# モデルロード用のコード（sample.pyからインポート）
import sys
sys.path.append("/Users/takeiyuto/IML2025K/yuto/chapter05")
from sample import model

# トークナイザーのロード
print("トークナイザーをロードしています...")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
print("トークナイザーのロードが完了しました")

# Zero-shot推論のためのプロンプト
prompt = """
以下の問題に答えてください。

9世紀に活躍した人物に関係するできごとについて述べた次のア～ウを年代の古い順に正しく並べよ。

ア　藤原時平は，策謀を用いて菅原道真を政界から追放した。
イ　嵯峨天皇は，藤原冬嗣らを蔵人頭に任命した。
ウ　藤原良房は，承和の変後，藤原氏の中での北家の優位を確立した。

年代の古い順に並べてください。
"""

print("推論を開始します...")

# トークン化と推論の準備
model_input = tokenizer(prompt, return_tensors="pt")
input_ids = model_input["input_ids"]

# 生成
with torch.no_grad():
    result = model.generate(
        input_ids,
        max_new_tokens=200,
        do_sample=False,
        num_beams=3,
        early_stopping=True
    )
    
    # 入力テキスト以降の生成部分を抽出
    result_text = result[0][input_ids.shape[-1]:]
    output = tokenizer.decode(result_text, skip_special_tokens=True)
    
    print("\n----- 生成結果 -----\n")
    print(output)
    
    # メモリを解放
    del input_ids
    del model_input
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

print("\n----- 推論完了 -----")