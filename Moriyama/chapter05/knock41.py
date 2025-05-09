from transformers import pipeline

# モデル読み込み
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Few-shotプロンプト（例題4つ + 本問）
examples = """以下は年代順に並べる歴史の問題とその正解例です。

問題1:
ア: 府知事・県令からなる地方官会議が設置された。
イ: 廃藩置県が実施された。
ウ: すべての藩主が天皇に領地と領民を返還した。
→ 正解: ウ→イ→ア

問題2:
ア: レザノフが長崎に来航し、ロシア船が樺太を攻撃。
イ: ゴローウニンが国後島に上陸。
ウ: ラクスマンが根室に来航し通商を求めた。
→ 正解: ウ→ア→イ

問題3:
ア: アヘン戦争が起きた。
イ: 異国船打払令が出された。
ウ: 桜田門外の変が起きた。
→ 正解: イ→ア→ウ

問題4:
ア: 三・一独立運動。
イ: 関東大震災後の混乱で殺傷事件。
ウ: 二十一カ条の要求。
→ 正解: ウ→ア→イ

問題5（本問）:
ア: 藤原時平は菅原道真を追放した。
イ: 嵯峨天皇は藤原冬嗣を蔵人頭に任命した。
ウ: 藤原良房が北家の優位を確立した。
"""

# 並び順の候補ラベル
labels = [
    "イ→ウ→ア",
    "イ→ア→ウ",
    "ウ→イ→ア",
    "ウ→ア→イ",
    "ア→イ→ウ",
    "ア→ウ→イ"
]

# 推論
result = classifier(examples, candidate_labels=labels)

# 最もスコアが高いものだけ表示
top_label = result['labels'][0]
top_score = result['scores'][0]

print("=== Few-Shot 推論の結果 ===")
print(f"推論結果: {top_label}（スコア: {top_score:.4f}）")

# === Few-Shot 推論の結果 ===
# 推論結果: ウ→ア→イ（スコア: 0.2419）