def solve_opposite_direction_problem():
    # 問題解決のための情報
    # 1. 東急大井町線の駅・急行停車駅の情報
    stations = [
        "溝の口", "高津", "二子新地", "二子玉川", "上野毛", 
        "等々力", "尾山台", "九品仏", "自由が丘", "緑が丘", 
        "大岡山", "北千束", "旗の台", "荏原町", "中延", 
        "戸越公園", "下神明", "大井町"
    ]
    
    express_stops = ["溝の口", "二子玉川", "自由が丘", "大岡山", "旗の台", "大井町"]
    
    # 2. 問題の条件から解答を導く
    jiyugaoka_index = stations.index("自由が丘")
    
    # 自由が丘から溝の口方面へ向かう（反対方向）急行停車駅を探す
    next_express_stop = None
    next_express_index = None
    for i in range(jiyugaoka_index - 1, -1, -1):
        if stations[i] in express_stops:
            next_express_stop = stations[i]
            next_express_index = i
            break
    
    # 自由が丘から目的地（大岡山）までのローカル停車駅数を計算
    jiyugaoka_index = stations.index("自由が丘")
    goal_station = "大岡山"  # 前の問題の答えにより、この駅が目的地と仮定
    goal_index = stations.index(goal_station)
    
    # 二子玉川（次の急行停車駅）から反対方向（大井町方面）の電車に乗って
    # 目的地（大岡山）までの駅数を計算
    stations_count = goal_index - next_express_index
    
    return {
        "next_express_stop": next_express_stop,
        "stations_count": stations_count,
        "stations_path": stations[next_express_index:goal_index+1]
    }

# 追加の問題文
additional_problem = """
さらに、つばめちゃんが自由が丘駅で乗り換えたとき、先ほどとは反対方向の急行電車に間違って乗車してしまった場合を考えます。
目的地の駅に向かうため、自由が丘の次の急行停車駅で降車した後、反対方向の各駅停車に乗車した場合、何駅先の駅で降りれば良いでしょうか？
"""

# Pythonコードで解を求める
solution = solve_opposite_direction_problem()

# モデルに与えるプロンプト
prompt = f"""以下の問題を解いてください。

{additional_problem}

この問題を解析すると：
1. つばめちゃんは自由が丘駅で東急大井町線の溝の口方面行きの急行に間違って乗った
2. 自由が丘の次の溝の口方面の急行停車駅（{solution["next_express_stop"]}駅）で降りた
3. そこから反対方向（大井町方面）の各駅停車に乗って目的地の大岡山駅に向かいたい
4. {solution["next_express_stop"]}駅から大岡山駅までは何駅あるか

東急大井町線の駅と急行停車駅の情報：
- 溝の口方面から大井町方面への順序: 溝の口→高津→二子新地→二子玉川→上野毛→等々力→尾山台→九品仏→自由が丘→緑が丘→大岡山→北千束→旗の台→荏原町→中延→戸越公園→下神明→大井町
- 急行停車駅: 溝の口、二子玉川、自由が丘、大岡山、旗の台、大井町
- 経路: {' → '.join(solution["stations_path"])}

この情報から、何駅先で降りればよいか答えてください。
"""

# 入力のエンコード 
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("生成開始...")

# 出力の生成
with torch.no_grad():
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=100,
        temperature=0.1,  # 低温度で確定的な出力
        num_return_sequences=1,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )

# 出力のデコード
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# プロンプトと生成された回答を分離
answer = generated_text[len(prompt):].strip()

print("\n--- 生成されたテキスト全体 ---")
print(generated_text)
print("\n--- 生成された回答部分 ---")
print(answer)

# 回答がない場合に備えて、Pythonの計算結果を使用
if not answer.strip():
    print("\n生成モデルからの回答を抽出できませんでした。")
    print(f"プログラムによる計算結果: {solution['stations_count']}駅先")
    final_answer = f"{solution['stations_count']}駅先"
else:
    final_answer = answer

print("\n最終回答:")
print(final_answer)
print(f"\n正解は: {solution['stations_count']}駅先")
print(f"経路: {' → '.join(solution['stations_path'])}")


"""
生成開始...

--- 生成されたテキスト全体 ---
以下の問題を解いてください。


さらに、つばめちゃんが自由が丘駅で乗り換えたとき、先ほどとは反対方向の急行電車に間違って乗車してしまった場合を考えます。
目的地の駅に向かうため、自由が丘の次の急行停車駅で降車した後、反対方向の各駅停車に乗車した場合、何駅先の駅で降りれば良いでしょうか？


この問題を解析すると：
1. つばめちゃんは自由が丘駅で東急大井町線の溝の口方面行きの急行に間違って乗った
2. 自由が丘の次の溝の口方面の急行停車駅（二子玉川駅）で降りた
3. そこから反対方向（大井町方面）の各駅停車に乗って目的地の大岡山駅に向かいたい
4. 二子玉川駅から大岡山駅までは何駅あるか

東急大井町線の駅と急行停車駅の情報：
- 溝の口方面から大井町方面への順序: 溝の口→高津→二子新地→二子玉川→上野毛→等々力→尾山台→九品仏→自由が丘→緑が丘→大岡山→北千束→旗の台→荏原町→中延→戸越公園→下神明→大井町
- 急行停車駅: 溝の口、二子玉川、自由が丘、大岡山、旗の台、大井町
- 経路: 二子玉川 → 上野毛 → 等々力 → 尾山台 → 九品仏 → 自由が丘 → 緑が丘 → 大岡山

この情報から、何駅先で降りればよいか答えてください。


--- 生成された回答部分 ---


生成モデルからの回答を抽出できませんでした。
プログラムによる計算結果: 7駅先

最終回答:
7駅先

正解は: 7駅先
経路: 二子玉川 → 上野毛 → 等々力 → 尾山台 → 九品仏 → 自由が丘 → 緑が丘 → 大岡山
"""