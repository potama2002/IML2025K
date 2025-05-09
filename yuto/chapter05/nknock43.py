import google.generativeai as genai
import os
import csv
from dotenv import load_dotenv
from pathlib import Path
import random
import time
import json

# 環境変数からAPIキーを読み込む
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# APIキーを設定
genai.configure(api_key=api_key)

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


def create_prompt(question, choices, prompt_type="standard", choice_symbols=None):
    """プロンプトを作成する"""
    if choice_symbols is None:
        choice_symbols = ["A", "B", "C", "D"]

    if prompt_type == "standard":
        prompt = f"""
以下の問題に対して、選択肢{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}の中から最も適切なものを1つ選んでください。
回答は選択肢の記号（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}）のみを返してください。

問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}
"""
    elif prompt_type == "detailed":
        prompt = f"""
以下の問題に対して、選択肢{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}の中から最も適切なものを1つ選んでください。
回答は選択肢の記号（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}）のみを返してください。
各選択肢を慎重に検討し、最も正確な回答を選んでください。

問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}
"""
    elif prompt_type == "concise":
        prompt = f"""
問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}

回答（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}のいずれか）：
"""

    return prompt


def shuffle_choices(choices, answer):
    """選択肢の順番をシャッフルする"""
    # 選択肢とインデックスのペアを作成
    indexed_choices = list(enumerate(choices))
    # シャッフル
    random.shuffle(indexed_choices)
    # 新しい順番の選択肢と、元のインデックスを取得
    new_choices = [c[1] for c in indexed_choices]
    # 正解のインデックスを更新
    old_index = ord(answer) - ord("A")
    new_index = indexed_choices.index((old_index, choices[old_index]))
    new_answer = chr(ord("A") + new_index)

    return new_choices, new_answer


def force_answer_to_d(choices, answer):
    """正解の選択肢をDに移動する"""
    ans_idx = ord(answer) - ord("A")
    correct_choice = choices[ans_idx]
    
    # 現在のD選択肢を取得
    d_choice = choices[3]
    
    # 新しい選択肢配列を作成
    new_choices = choices.copy()
    
    # 元の正解選択肢をD選択肢で置き換え
    new_choices[ans_idx] = d_choice
    
    # D選択肢を正解に置き換え
    new_choices[3] = correct_choice
    
    return new_choices, "D"


def save_cache(cache, filename):
    """キャッシュをファイルに保存する"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"キャッシュを保存しました: {len(cache)}件のエントリ")
    except Exception as e:
        print(f"キャッシュの保存に失敗しました: {e}")


def load_cache(filename):
    """キャッシュをファイルから読み込む"""
    if not os.path.exists(filename):
        return {}
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            cache = json.load(f)
        print(f"キャッシュを読み込みました: {len(cache)}件のエントリ")
        return cache
    except Exception as e:
        print(f"キャッシュの読み込みに失敗しました: {e}")
        return {}


def evaluate_model_with_settings(subject_key, settings, num_questions=10):
    """異なる設定でモデルの評価を行う（APIレート制限回避機能付き）"""
    # 科目名の取得
    if subject_key not in AVAILABLE_SUBJECTS:
        print(f"エラー: 科目 '{subject_key}' は利用できません。")
        print("利用可能な科目:")
        for key, name in AVAILABLE_SUBJECTS.items():
            print(f"  - {key}: {name}")
        return

    subject_name = AVAILABLE_SUBJECTS[subject_key]
    print(f"科目: {subject_name}")

    # データセットのパスを設定
    dataset_path = Path(f"JMMLU/JMMLU/{subject_key}.csv")

    # データセットの読み込み
    try:
        questions = load_jmmlu_data(dataset_path)
    except FileNotFoundError:
        print(f"エラー: 科目 '{subject_key}' のデータセットが見つかりません。")
        print("データセットをダウンロードしてください：")
        print("git clone https://github.com/nlp-waseda/JMMLU.git")
        return

    # 評価する問題数を制限
    if num_questions is None or num_questions > len(questions):
        questions = questions[:len(questions)]
    else:
        questions = questions[:num_questions]

    # 各設定での結果を格納する辞書
    results = {}
    
    # キャッシュの初期化
    cache_file = f"cache_{subject_key}.json"
    cache = load_cache(cache_file)

    # 各設定で評価
    for setting_name, setting in settings.items():
        print(f"\n設定: {setting_name}")
        print(f"温度: {setting.get('temperature', 0.7)}, プロンプトタイプ: {setting.get('prompt_type', 'standard')}")

        # モデルの設定
        model = genai.GenerativeModel(
            "gemini-1.5-flash-8b",
            generation_config={"temperature": setting.get("temperature", 0.7)},
        )

        correct_count = 0
        total_questions = len(questions)
        
        # バッチ処理のための設定
        batch_size = 3  # 一度に処理する問題数
        batch_wait = 10  # バッチ間の待機時間（秒）
        
        # 応答の記録（分析用）
        responses = []

        # バッチ処理
        for batch_start in range(0, total_questions, batch_size):
            batch_end = min(batch_start + batch_size, total_questions)
            batch = questions[batch_start:batch_end]
            
            print(f"\nバッチ処理: {batch_start+1}～{batch_end}/{total_questions}")

            for i, q in enumerate(batch, 1):
                q_idx = batch_start + i - 1  # 全体における問題のインデックス
                
                # 選択肢の処理
                choices = q["choices"].copy()  # 元の配列を変更しないようコピー
                answer = q["answer"]
                
                # 選択肢の順番をシャッフルするかどうか
                if setting.get("shuffle_choices", False):
                    choices, answer = shuffle_choices(choices, answer)
                
                # 正解をDに入れ替えるかどうか
                if setting.get("force_answer_to_d", False):
                    choices, answer = force_answer_to_d(choices, answer)
                
                # 選択肢の記号を変更するかどうか
                choice_symbols = setting.get("choice_symbols", ["A", "B", "C", "D"])

                # プロンプトの作成
                prompt = create_prompt(
                    q["question"],
                    choices,
                    setting.get("prompt_type", "standard"),
                    choice_symbols,
                )
                
                # キャッシュキーの作成
                cache_key = f"{setting_name}_{q['question']}_{','.join(choices)}"
                
                # APIリクエストの試行回数
                max_retries = 3
                retry_count = 0
                
                # キャッシュに存在する場合はそれを使用
                if cache_key in cache:
                    model_answer = cache[cache_key]
                    print(f"\rキャッシュから回答を取得: {model_answer}", end="")
                else:
                    # リクエスト間のウェイト
                    if q_idx > batch_start:
                        time.sleep(2)  # 同じバッチ内の前のリクエストから2秒待機
                    
                    # API呼び出しと再試行ロジック
                    while retry_count < max_retries:
                        try:
                            # APIリクエストの送信
                            response = model.generate_content(prompt)
                            model_answer = response.text.strip().upper()
                            
                            # キャッシュに保存
                            cache[cache_key] = model_answer
                            if q_idx % 5 == 0:  # 5問ごとにキャッシュを保存
                                save_cache(cache, cache_file)
                                
                            break  # 成功したらループを抜ける
                            
                        except Exception as e:
                            retry_count += 1
                            if retry_count < max_retries:
                                wait_time = 5 * retry_count  # リトライごとに待機時間を増やす
                                print(f"\nAPIエラー: {e}. {wait_time}秒待機してリトライします ({retry_count}/{max_retries})")
                                time.sleep(wait_time)
                            else:
                                print(f"\n最大リトライ回数に達しました。エラー: {e}")
                                model_answer = "ERROR"  # エラーの場合は不正解としてカウント
                
                # 応答を記録
                responses.append({
                    "question_idx": q_idx,
                    "question": q["question"],
                    "original_choices": q["choices"],
                    "presented_choices": choices,
                    "original_answer": q["answer"],
                    "expected_answer": answer,
                    "model_answer": model_answer
                })

                # 選択肢の記号が変更されている場合、回答を変換
                if choice_symbols != ["A", "B", "C", "D"]:
                    # 元の記号に変換
                    symbol_map = {
                        choice_symbols[i]: chr(ord("A") + i) for i in range(4)
                    }
                    model_answer = symbol_map.get(model_answer, model_answer)

                # 正解判定
                is_correct = model_answer == answer
                correct_count += int(is_correct)

                # 進捗表示
                print(f"\r進捗: {q_idx+1}/{total_questions} (正解率: {correct_count / (q_idx+1) * 100:.1f}%)", end="")

            # バッチ間の待機（最後のバッチ以外）
            if batch_end < total_questions:
                print(f"\nAPIレート制限回避のため {batch_wait}秒 待機します...")
                time.sleep(batch_wait)
        
        # 最終結果の表示
        final_accuracy = correct_count / total_questions * 100
        print("\n\n評価結果:")
        print(f"正解数: {correct_count}/{total_questions}")
        print(f"正解率: {final_accuracy:.1f}%")

        # 結果を保存
        results[setting_name] = {
            "correct_count": correct_count,
            "total_questions": total_questions,
            "accuracy": final_accuracy,
            "responses": responses
        }
        
        # 設定間の待機
        if setting_name != list(settings.keys())[-1]:  # 最後の設定でなければ
            print(f"\n次の設定に進む前に30秒待機します...")
            time.sleep(30)
    
    # 最終的なキャッシュの保存
    save_cache(cache, cache_file)
    
    # 回答の分布を分析
    analyze_answer_distribution(results)
            
    return results


def analyze_answer_distribution(results):
    """回答の分布を分析する"""
    print("\n回答分布の分析:")
    
    for setting_name, result in results.items():
        if "responses" not in result:
            continue
            
        responses = result["responses"]
        
        # 回答の分布をカウント
        answer_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "ERROR": 0, "OTHER": 0}
        
        for resp in responses:
            model_answer = resp["model_answer"]
            if model_answer in answer_counts:
                answer_counts[model_answer] += 1
            else:
                answer_counts["OTHER"] += 1
        
        # 分布の表示
        print(f"\n設定: {setting_name}")
        total = sum(answer_counts.values())
        for answer, count in answer_counts.items():
            percentage = (count / total) * 100 if total > 0 else 0
            print(f"{answer}: {count} ({percentage:.1f}%)")


def run_experiments(subject_key, num_questions=10):
    """様々な実験設定で評価を実行する"""
    # 実験設定
    settings = {
        "標準設定": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "低温度": {
            "temperature": 0.1,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "高温度": {
            "temperature": 1.0,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "詳細プロンプト": {
            "temperature": 0.7,
            "prompt_type": "detailed",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "簡潔プロンプト": {
            "temperature": 0.7,
            "prompt_type": "concise",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "選択肢シャッフル": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": True,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "数字記号": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["1", "2", "3", "4"],
        },
        "正解をDに固定": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "force_answer_to_d": True,
            "choice_symbols": ["A", "B", "C", "D"],
        },
    }

    # 実験結果を保存するファイル名
    results_file = f"experiment_results_{subject_key}.json"

    # 評価実行
    results = evaluate_model_with_settings(subject_key, settings, num_questions)

    # 結果の比較
    print("\n\n実験結果の比較:")
    print("=" * 60)
    print(f"{'設定名':<20} {'正解数':<10} {'正解率':<10}")
    print("-" * 60)

    for setting_name, result in results.items():
        print(
            f"{setting_name:<20} {result['correct_count']}/{result['total_questions']:<10} {result['accuracy']:.1f}%"
        )

    print("=" * 60)
    
    # 結果をファイルに保存
    try:
        with open(results_file, "w", encoding="utf-8") as f:
            # 保存前に各設定からresponses項目を削除（サイズ削減のため）
            save_results = {}
            for setting_name, result in results.items():
                save_results[setting_name] = {
                    "correct_count": result["correct_count"],
                    "total_questions": result["total_questions"],
                    "accuracy": result["accuracy"]
                }
            json.dump(save_results, f, ensure_ascii=False, indent=2)
        print(f"\n実験結果を保存しました: {results_file}")
    except Exception as e:
        print(f"\n実験結果の保存に失敗しました: {e}")
    
    # CSVファイルにも保存
    csv_file = f"experiment_results_{subject_key}.csv"
    try:
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["設定名", "正解数", "問題数", "正解率"])
            for setting_name, result in results.items():
                writer.writerow([
                    setting_name, 
                    result["correct_count"], 
                    result["total_questions"], 
                    f"{result['accuracy']:.1f}%"
                ])
        print(f"実験結果をCSVファイルにも保存しました: {csv_file}")
    except Exception as e:
        print(f"CSVファイルの保存に失敗しました: {e}")


if __name__ == "__main__":
    # 科目を選択（例: 'world_history'）
    subject = "world_history"
    # 評価する問題数
    num_questions = 10  # 実験用に少ない問題数で実行

    run_experiments(subject, num_questions)


    """科目: 世界史

設定: 標準設定
温度: 0.7, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 1件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 6件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 低温度
温度: 0.1, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 11件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 16件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 高温度
温度: 1.0, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 21件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 26件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 詳細プロンプト
温度: 0.7, プロンプトタイプ: detailed

バッチ処理: 1～3/10
キャッシュを保存しました: 31件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 36件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 簡潔プロンプト
温度: 0.7, プロンプトタイプ: concise

バッチ処理: 1～3/10
キャッシュを保存しました: 41件のエントリ
進捗: 3/10 (正解率: 0.0%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 0.0%)キャッシュを保存しました: 46件のエントリ
進捗: 6/10 (正解率: 0.0%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 0.0%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 0.0%)

評価結果:
正解数: 0/10
正解率: 0.0%

次の設定に進む前に30秒待機します...

設定: 選択肢シャッフル
温度: 0.7, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 51件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 56件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 数字記号
温度: 0.7, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 61件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 66件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%

次の設定に進む前に30秒待機します...

設定: 正解をDに固定
温度: 0.7, プロンプトタイプ: standard

バッチ処理: 1～3/10
キャッシュを保存しました: 71件のエントリ
進捗: 3/10 (正解率: 66.7%))
APIレート制限回避のため 10秒 待機します...

バッチ処理: 4～6/10
進捗: 5/10 (正解率: 80.0%)キャッシュを保存しました: 76件のエントリ
進捗: 6/10 (正解率: 83.3%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 7～9/10
進捗: 9/10 (正解率: 88.9%)
APIレート制限回避のため 10秒 待機します...

バッチ処理: 10～10/10
進捗: 10/10 (正解率: 90.0%)

評価結果:
正解数: 9/10
正解率: 90.0%
キャッシュを保存しました: 80件のエントリ

回答分布の分析:

設定: 標準設定
A: 1 (10.0%)
B: 3 (30.0%)
C: 3 (30.0%)
D: 3 (30.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)

設定: 低温度
A: 1 (10.0%)
B: 3 (30.0%)
C: 3 (30.0%)
D: 3 (30.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)

設定: 高温度
A: 1 (10.0%)
B: 3 (30.0%)
C: 3 (30.0%)
D: 3 (30.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)

設定: 詳細プロンプト
A: 1 (10.0%)
B: 3 (30.0%)
C: 3 (30.0%)
D: 3 (30.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)

設定: 簡潔プロンプト
A: 0 (0.0%)
B: 0 (0.0%)
C: 0 (0.0%)
D: 0 (0.0%)
ERROR: 0 (0.0%)
OTHER: 10 (100.0%)

設定: 選択肢シャッフル
A: 1 (10.0%)
B: 3 (30.0%)
C: 4 (40.0%)
D: 2 (20.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)

設定: 数字記号
A: 0 (0.0%)
B: 0 (0.0%)
C: 0 (0.0%)
D: 0 (0.0%)
ERROR: 0 (0.0%)
OTHER: 10 (100.0%)

設定: 正解をDに固定
A: 1 (10.0%)
B: 0 (0.0%)
C: 0 (0.0%)
D: 9 (90.0%)
ERROR: 0 (0.0%)
OTHER: 0 (0.0%)


実験結果の比較:
============================================================
設定名                  正解数        正解率       
------------------------------------------------------------
標準設定                 9/10         90.0%
低温度                  9/10         90.0%
高温度                  9/10         90.0%
詳細プロンプト              9/10         90.0%
簡潔プロンプト              0/10         0.0%
選択肢シャッフル             9/10         90.0%
数字記号                 9/10         90.0%
正解をDに固定              9/10         90.0%
============================================================

実験結果を保存しました: experiment_results_world_history.json
実験結果をCSVファイルにも保存しました: experiment_results_world_history.csv"""