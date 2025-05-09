import google.generativeai as genai
import os
import csv
import json
import time
from dotenv import load_dotenv
from pathlib import Path

# 環境変数からAPIキーを読み込む
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# APIキーを設定
genai.configure(api_key=api_key)

# モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# 利用可能な科目のリスト
AVAILABLE_SUBJECTS = {
    "world_history": "世界史",
    "japanese_history": "日本史",
    "philosophy": "哲学",
    "sociology": "社会学",
    "high_school_physics": "高校物理",
    "high_school_mathematics": "高校数学",
    "high_school_chemistry": "高校化学",
    "high_school_biology": "高校生物",
    "college_physics": "大学物理",
    "college_mathematics": "大学数学",
    "college_chemistry": "大学化学",
    "college_biology": "大学生物学",
    "computer_security": "コンピュータセキュリティ",
    "machine_learning": "機械学習",
    "high_school_computer_science": "高校情報科学",
    "college_computer_science": "大学コンピュータ科学",
    "high_school_psychology": "高校心理学",
    "professional_psychology": "専門心理学",
    "high_school_statistics": "高校統計学",
    "econometrics": "計量経済学",
    "high_school_microeconomics": "高校ミクロ経済学",
    "high_school_macroeconomics": "高校マクロ経済学",
    "management": "経営学",
    "marketing": "マーケティング",
    "business_ethics": "ビジネス倫理",
    "professional_accounting": "専門会計",
    "professional_medicine": "専門医学",
    "college_medicine": "大学医学",
    "clinical_knowledge": "臨床知識",
    "medical_genetics": "医学遺伝学",
    "anatomy": "解剖学",
    "human_aging": "人間の老化",
    "nutrition": "栄養学",
    "high_school_geography": "高校地理",
    "high_school_european_history": "高校ヨーロッパ史",
    "international_law": "国際法",
    "jurisprudence": "法理学",
    "formal_logic": "形式論理",
    "logical_fallacies": "論理学",
    "moral_disputes": "倫理的議論",
    "world_religions": "世界宗教",
    "human_sexuality": "セクシュアリティ",
    "security_studies": "セキュリティ研究",
    "electrical_engineering": "電気工学",
    "conceptual_physics": "概念物理学",
    "astronomy": "天文学",
    "prehistory": "先史学",
    "global_facts": "世界事実",
    "miscellaneous": "雑学",
    "abstract_algebra": "抽象代数",
    "elementary_mathematics": "初等数学",
    "virology": "ウイルス学",
    "public_relations": "公共関係",
}


def load_jmmlu_data(file_path):
    """JMMLUのデータセットを読み込む"""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 6:  # 問題、選択肢A、B、C、D、正解の6列があることを確認
                data.append({"question": row[0], "choices": row[1:5], "answer": row[5]})
    return data


def create_prompt(question, choices):
    """プロンプトを作成する"""
    prompt = f"""
以下の問題に対して、選択肢A、B、C、Dの中から最も適切なものを1つ選んでください。
回答は選択肢のアルファベット（A、B、C、D）のみを返してください。

問題：{question}

選択肢：
A. {choices[0]}
B. {choices[1]}
C. {choices[2]}
D. {choices[3]}
"""
    return prompt


def evaluate_model(subject_key, num_questions=None, batch_size=10, max_retries=3, delay_seconds=1):
    """モデルの評価を行う (エラー処理強化版)"""
    # 科目名の取得
    if subject_key not in AVAILABLE_SUBJECTS:
        print(f"エラー: 科目 '{subject_key}' は利用できません。")
        print("利用可能な科目:")
        for key, name in AVAILABLE_SUBJECTS.items():
            print(f"  - {key}: {name}")
        return

    subject_name = AVAILABLE_SUBJECTS[subject_key]

    # データセットのパスを設定
    dataset_path = Path(f"JMMLU/JMMLU/{subject_key}.csv")

    # データセットの読み込み
    try:
        all_questions = load_jmmlu_data(dataset_path)
    except FileNotFoundError:
        print(f"エラー: 科目 '{subject_key}' のデータセットが見つかりません。")
        print("データセットをダウンロードしてください：")
        print("git clone https://github.com/nlp-waseda/JMMLU.git")
        return

    # 評価する問題数を制限
    if num_questions is not None:
        questions = all_questions[:num_questions]
    else:
        questions = all_questions

    # 結果を保存するファイル
    results_file = f"results_{subject_key}.json"
    
    # 既存の結果があれば読み込む
    results = {}
    if os.path.exists(results_file):
        with open(results_file, 'r', encoding='utf-8') as f:
            try:
                results = json.load(f)
                print(f"保存された結果を読み込みました: {len(results)}問")
            except json.JSONDecodeError:
                print("保存ファイルの読み込みに失敗しました。新しく作成します。")
    
    # 処理済みの問題数と正解数を計算
    processed_indices = [int(idx) for idx in results.keys()]
    correct_count = sum(int(val) for val in results.values())
    
    total_questions = len(questions)
    total_available = len(all_questions)
    
    print(f"科目: {subject_name}")
    print(f"問題数: {total_questions} (全{total_available}問中)")
    print(f"すでに処理済み: {len(processed_indices)}問")
    print("評価を開始します...")
    
    # 全ての問題を処理
    for i, q in enumerate(questions, 1):
        # すでに処理済みならスキップ
        if str(i) in results:
            continue
            
        prompt = create_prompt(q["question"], q["choices"])
        
        # 再試行ロジック
        retries = 0
        success = False
        
        while retries < max_retries and not success:
            try:
                # 少し待機してからAPIリクエスト
                time.sleep(delay_seconds)
                response = model.generate_content(prompt)
                answer = response.text.strip().upper()
                
                # 正解判定
                is_correct = answer == q["answer"]
                results[str(i)] = int(is_correct)
                
                # 正解数を更新
                correct_count = sum(int(val) for val in results.values())
                processed_count = len(results)
                
                # 進捗表示
                success_rate = correct_count / processed_count * 100
                print(f"\r進捗: {processed_count}/{total_questions} (正解率: {success_rate:.1f}%)", end="")
                
                success = True
                
            except Exception as e:
                retries += 1
                print(f"\n問題 {i} でエラー ({retries}/{max_retries}): {e}")
                
                if retries < max_retries:
                    wait_time = delay_seconds * (2 ** retries)  # 指数バックオフ
                    print(f"{wait_time}秒待機してから再試行します...")
                    time.sleep(wait_time)
                else:
                    print(f"問題 {i} は最大再試行回数に達しました。スキップします。")
                    # 処理に失敗した問題も記録（値を-1として）
                    results[str(i)] = -1  # -1 は処理失敗を示す
        
        # バッチごとに結果を保存
        if len(results) % batch_size == 0 or i == total_questions:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f)
            print(f"\n{len(results)}問まで処理しました。結果を保存しました。")
    
    # 最終結果の表示
    # 処理失敗(-1)の項目を除いて集計
    valid_results = {k: v for k, v in results.items() if v != -1}
    processed_count = len(valid_results)
    correct_count = sum(valid_results.values())
    
    if processed_count > 0:
        final_accuracy = correct_count / processed_count * 100
        print("\n\n評価結果:")
        print(f"正解数: {correct_count}/{processed_count}")
        print(f"正解率: {final_accuracy:.1f}%")
        
        # 処理失敗の数も表示
        failed_count = len(results) - processed_count
        if failed_count > 0:
            print(f"処理失敗: {failed_count}問")
    else:
        print("\n\n評価結果: 処理に成功した問題がありません。")


if __name__ == "__main__":
    # 科目を選択（例: 'world_history'）
    subject = "world_history"
    # 評価する問題数を全問に設定
    num_questions = None  # Noneを指定すると全問題を評価
    # バッチサイズ（何問ごとに結果を保存するか）
    batch_size = 5
    # 最大再試行回数
    max_retries = 3
    # リクエスト間の待機時間（秒）
    delay_seconds = 2
    
    # 強化版の評価関数を呼び出す
    evaluate_model(
        subject,
        num_questions=num_questions,
        batch_size=batch_size,
        max_retries=max_retries,
        delay_seconds=delay_seconds
    )

    """科目: 世界史
問題数: 150 (全150問中)
すでに処理済み: 0問
評価を開始します...
進捗: 5/150 (正解率: 80.0%))
5問まで処理しました。結果を保存しました。
進捗: 10/150 (正解率: 90.0%)
10問まで処理しました。結果を保存しました。
進捗: 15/150 (正解率: 86.7%)
15問まで処理しました。結果を保存しました。
進捗: 20/150 (正解率: 90.0%)
20問まで処理しました。結果を保存しました。
進捗: 25/150 (正解率: 92.0%)
25問まで処理しました。結果を保存しました。
進捗: 30/150 (正解率: 90.0%)
30問まで処理しました。結果を保存しました。
進捗: 35/150 (正解率: 85.7%)
35問まで処理しました。結果を保存しました。
進捗: 40/150 (正解率: 87.5%)
40問まで処理しました。結果を保存しました。
進捗: 45/150 (正解率: 86.7%)
45問まで処理しました。結果を保存しました。
進捗: 50/150 (正解率: 86.0%)
50問まで処理しました。結果を保存しました。
進捗: 55/150 (正解率: 87.3%)
55問まで処理しました。結果を保存しました。
進捗: 60/150 (正解率: 88.3%)
60問まで処理しました。結果を保存しました。
進捗: 65/150 (正解率: 89.2%)
65問まで処理しました。結果を保存しました。
進捗: 70/150 (正解率: 88.6%)
70問まで処理しました。結果を保存しました。
進捗: 75/150 (正解率: 89.3%)
75問まで処理しました。結果を保存しました。
進捗: 80/150 (正解率: 90.0%)
80問まで処理しました。結果を保存しました。
進捗: 85/150 (正解率: 89.4%)
85問まで処理しました。結果を保存しました。
進捗: 90/150 (正解率: 90.0%)
90問まで処理しました。結果を保存しました。
進捗: 95/150 (正解率: 90.5%)
95問まで処理しました。結果を保存しました。
進捗: 100/150 (正解率: 90.0%)
100問まで処理しました。結果を保存しました。
進捗: 105/150 (正解率: 90.5%)
105問まで処理しました。結果を保存しました。
進捗: 110/150 (正解率: 90.9%)
110問まで処理しました。結果を保存しました。
進捗: 115/150 (正解率: 91.3%)
115問まで処理しました。結果を保存しました。
進捗: 120/150 (正解率: 90.8%)
120問まで処理しました。結果を保存しました。
進捗: 125/150 (正解率: 91.2%)
125問まで処理しました。結果を保存しました。
進捗: 130/150 (正解率: 90.0%)
130問まで処理しました。結果を保存しました。
進捗: 135/150 (正解率: 90.4%)
135問まで処理しました。結果を保存しました。
進捗: 140/150 (正解率: 89.3%)
140問まで処理しました。結果を保存しました。
進捗: 145/150 (正解率: 89.7%)
145問まで処理しました。結果を保存しました。
進捗: 150/150 (正解率: 89.3%)
150問まで処理しました。結果を保存しました。


評価結果:
正解数: 134/150
正解率: 89.3%"""