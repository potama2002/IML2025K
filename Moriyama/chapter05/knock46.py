from transformers import GPTNeoXTokenizerFast, GPTNeoXForCausalLM
import torch

model_name = "cyberagent/open-calm-3b"  # もしくは他の GPT-NeoX 系

# トークナイザとモデルを明示的に指定
tokenizer = GPTNeoXTokenizerFast.from_pretrained(model_name)
model = GPTNeoXForCausalLM.from_pretrained(model_name)
model.to("cpu")
model.eval()

prompt = """お題：通勤電車

以下のお題に基づいて、川柳（五・七・五の17音の短詩）を10個作ってください。
同じ句の繰り返しは避けて、毎回違う視点で詠んでください。

例:
1. 朝ラッシュ 押されて乗った 知らぬ駅
2. 吊り革に 掴まるたびに 夢遠く
3. 無言でも 通じる目線 満員車両

それでは本番です。
"""



# トークナイズ
inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

# 生成
output = model.generate(
    **inputs,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.8,
    top_p=0.95,
    pad_token_id=tokenizer.eos_token_id
)

print("=== 川柳 ===")
print(tokenizer.decode(output[0], skip_special_tokens=True))
