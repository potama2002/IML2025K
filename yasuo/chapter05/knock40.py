
# 40
prompt = """
[問題]に対する[答え]を[選択肢]の中から選んでください。
9世紀に活躍した人物に関係するできごとについて述べた次のア～ウを年代の古い順に正しく並べよ。

ア　藤原時平は，策謀を用いて菅原道真を政界から追放した。
イ　嵯峨天皇は，藤原冬嗣らを蔵人頭に任命した。
ウ　藤原良房は，承和の変後，藤原氏の中での北家の優位を確立した。
[選択肢]:[ア，イ，ウ]
[答え]:"""

for i in range(3):
  model_input = tokenizer(prompt, return_tensors="pt").to(model.device)
  input_ids = model_input["input_ids"]

  with torch.no_grad():
    result = model.generate(
                input_ids,
                max_new_tokens=300,
                # eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
    result = result[0][input_ids.shape[-1]:]
    output = tokenizer.decode(result, skip_special_tokens=True)
    print("\n-----生成結果-----\n", output.split("[問題]")[0])

    del input_ids
    del model_input
    torch.cuda.empty_cache()

"""
The attention mask and the pad token id were not set. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.
The attention mask and the pad token id were not set. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.

-----生成結果-----
 [ア，ウ，イ]


The attention mask and the pad token id were not set. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.

-----生成結果-----
 [ウ，イ，ア]



-----生成結果-----
 [ウ，イ，ア]
"""