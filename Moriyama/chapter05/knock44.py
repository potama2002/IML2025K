from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "rinna/japanese-gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name).to("cpu").eval()

# 背景知識 + 問題文 + 指示（プロンプト全体）
prompt = """東急大井町線の急行は以下の駅に停車します：
大井町、旗の台、大岡山、自由が丘、二子玉川、溝の口。

各駅停車は大岡山 → 緑が丘 → 自由が丘 → 九品仏 → 尾山台 → 等々力 → 上野毛 → 二子玉川…

つばめちゃんは渋谷駅から東急東横線に乗り、自由が丘駅で乗り換えました。
東急大井町線の大井町方面の電車に乗り換えたとき、各駅停車に乗車すべきところ、
間違えて急行に乗車してしまったことに気付きました。自由が丘の次の急行停車駅で
降車し、反対方向の電車で一駅戻った駅がつばめちゃんの目的地でした。目的地の駅の
名前を答えてください。

駅名だけを答えてください。
"""

# トークナイズと生成
inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
outputs = model.generate(
    **inputs,
    max_new_tokens=30,
    do_sample=True,
    temperature=0.7,
    top_p=0.95,
    pad_token_id=tokenizer.eos_token_id
)

print("=== 応答 ===")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
