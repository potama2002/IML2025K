# 45
# 夏祭りと花火をテーマにした川柳生成のプロンプト
prompt = """「夏祭り」と「花火」をテーマにした川柳を10個生成してください。川柳は5-7-5の音節構造を持つ日本の短詩形です。
季節感や情緒、夏の風物詩としての魅力が伝わる作品にしてください。それぞれの川柳には短い解説も付けてください。

例えば：
「花火見て 子どもの顔に 咲く笑顔」
解説：花火を見上げる子どもの無邪気な表情を咲く花に例えた一句

以下、「夏祭り」と「花火」をテーマにした川柳10個を出力してください。それぞれに簡潔な解説を付けてください。"""

# 入力のエンコード 
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("川柳の生成を開始...")

# より創造的な出力を得るため、温度を上げる
with torch.no_grad():
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=1000,  # より長い出力を許可
        temperature=0.8,      # 創造性のために温度を上げる
        num_return_sequences=1,
        top_p=0.95,
        repetition_penalty=1.2,  # 繰り返しを減らす
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )

# 出力のデコード
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# プロンプトと生成された回答を分離
answer = generated_text[len(prompt):].strip()

print("\n--- 生成された川柳10選 ---")
print(answer)

"""
川柳の生成を開始...

--- 生成された川柳10選 ---
"""