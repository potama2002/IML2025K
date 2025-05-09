import pandas as pd
import random
from transformers import pipeline

# モデル読み込み
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# CSVファイルパス（列名なし想定）
csv_path = "/Users/takerumoriyama/Library/CloudStorage/GoogleDrive-tacom394@gmail.com/マイドライブ/vsCode/IML2025K/Moriyama/JMMLU/JMMLU/japanese_history.csv"
df = pd.read_csv(csv_path, header=None)

# 実験パラメータ
num_trials = 2  # シャッフル回数

# 各試行ごとの正答数を記録
correct_counts = [0 for _ in range(num_trials)]

for _, row in df.iterrows():
    question = row[0]
    original_choices = [row[1], row[2], row[3], row[4]]
    correct_label = row[5].strip()

    for trial in range(num_trials):
        shuffled = original_choices.copy()
        random.shuffle(shuffled)

        result = classifier(question, candidate_labels=shuffled)
        prediction_text = result['labels'][0]

        # オリジナル選択肢に対応するラベルを特定
        predicted_label = [k for k, v in zip(['A', 'B', 'C', 'D'], original_choices) if v == prediction_text]
        predicted_label = predicted_label[0] if predicted_label else "?"

        if predicted_label == correct_label:
            correct_counts[trial] += 1

# ✅ 出力
for trial in range(num_trials):
    total = len(df)
    accuracy = correct_counts[trial] / total * 100
    print(f"[シャッフル{trial+1}回目] 正答率: {accuracy:.2f}%")

print(f"※ 各問題に対して選択肢の順番をランダムに2回変えて推論")

# [シャッフル1回目] 正答率: 24.00%
# [シャッフル2回目] 正答率: 24.00%
# ※ 各問題に対して選択肢の順番をランダムに2回変えて推論