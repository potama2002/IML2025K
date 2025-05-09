from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# モデルとトークナイザーをロード（pipelineは使わない）
model_name = "rinna/japanese-gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # ← 重要: fast tokenizer を無効化
model = AutoModelForCausalLM.from_pretrained(model_name)

# CPUで動作させる
device = torch.device("cpu")
model = model.to(device)

# プロンプト
prompt = (
    "つばめちゃんは渋谷駅から東急東横線に乗り、自由が丘駅で乗り換えました。東急大井町線の大井町方面の電車に乗り換えたとき、各駅停車に乗車すべきところ、間違えて急行に乗車してしまったことに気付きました。自由が丘の次の急行停車駅で降車し、反対方向の電車で一駅戻った駅がつばめちゃんの目的地でした。目的地の駅の名前を答えてください。さらに、つばめちゃんが自由が丘駅で乗り換えたとき、先ほどとは反対方向の急行電車に間違って乗車してしまった場合を考えます。目的地の駅に向かうため、自由が丘の次の急行停車駅で降車した後、反対方向の各駅停車に乗車した場合、何駅先の駅で降りれば良いでしょうか？"
)

# トークナイズ
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# テキスト生成
output = model.generate(
    **inputs,
    max_length=128,
    do_sample=True,
    temperature=0.7,
    top_p=0.95,
    pad_token_id=tokenizer.eos_token_id
)

# 結果表示
print("=== 応答 ===")
print(tokenizer.decode(output[0], skip_special_tokens=True))
