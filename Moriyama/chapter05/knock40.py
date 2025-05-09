from transformers import pipeline

# モデル読み込み
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Zero-shot対象の文章（第40問）
sequence = (
    "以下の3つの出来事を年代の古い順に並べなさい：\n"
    "ア：藤原時平は策謀を用いて菅原道真を政界から追放した。\n"
    "イ：嵯峨天皇は藤原冬嗣らを蔵人頭に任命した。\n"
    "ウ：藤原良房は承和の変後、藤原氏の中での北家の優位を確立した。"
)

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
result = classifier(sequence, candidate_labels=labels)

# 最もスコアが高いものを取得
top_label = result['labels'][0]
top_score = result['scores'][0]

# 出力
print("=== 最も高いスコアの解答 ===")
print(f"推論結果: {top_label}（スコア: {top_score:.4f}）")


# === 最も高いスコアの解答 ===
# 推論結果: ア→イ→ウ（スコア: 0.1886）