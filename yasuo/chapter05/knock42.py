# 42

import pandas as pd
import torch
import re
from tqdm.notebook import tqdm
import os

# JMMLUリポジトリのクローン（まだ存在しない場合）
if not os.path.exists("./JMMLU"):
    print("JMMLUリポジトリをクローン中...")
    !git clone https://github.com/nlp-waseda/JMMLU.git

def generate_prompt(question, choices):
    """プロンプトを生成する関数"""
    prompt = f"""以下の問題に対して、選択肢A、B、C、Dから最も適切な答えを1つ選んでください。
選択肢を選ぶ理由を簡潔に説明し、最後に「答え: 」の後に選んだ選択肢（A、B、C、Dのいずれか）のみを記入してください。

問題: {question}

選択肢:
A. {choices[0]}
B. {choices[1]}
C. {choices[2]}
D. {choices[3]}

"""
    return prompt

def extract_answer(text):
    """モデルの出力から回答を抽出する関数"""
    # パターン1: 「答え: X」という形式
    pattern1 = r"答え\s*[:：]\s*([ABCD])"
    match1 = re.search(pattern1, text)
    if match1:
        return match1.group(1)

    # パターン2: 最後の行に単独で「A」「B」「C」「D」のいずれかがある
    pattern2 = r"([ABCD])\s*$"
    match2 = re.search(pattern2, text)
    if match2:
        return match2.group(1)

    # パターン3: 文中に「選択肢はX」「Xが正解」などの表現がある
    pattern3 = r"選択肢[はがのはABCD]*\s*([ABCD])"
    match3 = re.search(pattern3, text)
    if match3:
        return match3.group(1)

    # テキスト全体からA,B,C,Dのみを探す
    choices = re.findall(r'\b[ABCD]\b', text)
    if choices:
        # 最も頻繁に出現する選択肢を回答とする
        return max(set(choices), key=choices.count)

    return None

def evaluate_jmmlu_computer_security(model, tokenizer):
    """JMMLUのコンピュータセキュリティデータセットを評価する関数"""
    # CSVファイルのパス
    csv_path = "./JMMLU/JMMLU/computer_security.csv"

    # CSVファイル読み込み
    print(f"コンピュータセキュリティCSV読み込み中: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"データセット読み込み完了。問題数: {len(df)}問")

    # カラム名の確認
    print(f"カラム名: {df.columns.tolist()}")

    # データ形式の確認（最初の行）
    first_row = df.iloc[0].tolist()
    print("\n最初の問題のデータ:")
    for i, value in enumerate(first_row):
        print(f"列{i}: {value}")

    # 評価用データの準備
    correct = 0
    total = 0

    # 進捗表示用
    print("\n評価開始 - 全99問のコンピュータセキュリティ問題")

    # 各問題に対して評価
    for i in tqdm(range(len(df)), desc="Evaluating"):
        row = df.iloc[i].tolist()

        # 行の形式に応じて問題と選択肢を抽出
        question = row[0]  # 最初の列を問題文とする
        choices = row[1:5]  # 2-5列目を選択肢とする
        correct_answer = row[5]  # 6列目を正解とする

        # プロンプト生成
        prompt = generate_prompt(question, choices)

        # トークナイズとモデル入力の準備
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # 生成
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=True,
                top_p=0.95,
                top_k=50,
                pad_token_id=tokenizer.eos_token_id
            )

        # 出力のデコード
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # プロンプト部分を削除して回答のみを取得
        predicted_text = generated_text[len(prompt):]

        # 回答の抽出
        predicted_answer = extract_answer(predicted_text)

        # 正解判定
        is_correct = (predicted_answer == correct_answer)
        if is_correct:
            correct += 1
        total += 1

        # 25問ごとに進捗状況を表示
        if (i + 1) % 25 == 0:
            print(f"進捗: {i+1}/99問完了、現在の正解率: {correct}/{total} ({correct/total:.4f})")

    # 最終結果の表示
    accuracy = correct / total
    print(f"\n評価完了！")
    print(f"モデル: elyza/ELYZA-japanese-Llama-2-7b")
    print(f"データセット: JMMLU computer_security")
    print(f"正解数: {correct}/{total}問")
    print(f"正解率: {accuracy:.4f} ({accuracy*100:.2f}%)")

    return correct, total, accuracy

# メイン実行部分
# モデルとトークナイザーはすでに読み込まれていると仮定
# model = すでに読み込まれているモデル
# tokenizer = すでに読み込まれているトークナイザー

# 評価の実行
correct, total, accuracy = evaluate_jmmlu_computer_security(model, tokenizer)

"""
JMMLUリポジトリをクローン中...
Cloning into 'JMMLU'...
remote: Enumerating objects: 408, done.
remote: Counting objects: 100% (134/134), done.
remote: Compressing objects: 100% (128/128), done.
remote: Total 408 (delta 73), reused 14 (delta 6), pack-reused 274 (from 1)
Receiving objects: 100% (408/408), 1.46 MiB | 4.26 MiB/s, done.
Resolving deltas: 100% (211/211), done.
コンピュータセキュリティCSV読み込み中: ./JMMLU/JMMLU/computer_security.csv
データセット読み込み完了。問題数: 98問
カラム名: ['クライアントとサーバー間でTLS接続が正常に確立されたとする。セッションの確立には、サーバー証明書のチェックとディフィー・ヘルマン交換の実行が含まれるが、クライアントはクライアント証明書を提供していない。さらに、クライアントとサーバーは正直であり、クライアントとサーバーは鍵を漏洩せず、暗号は良好であると仮定する。TLSが防御する攻撃は次のうちどれか? \n1. クライアントが以前に送信したバイトを再生する攻撃者。\n2. サーバーになりすます攻撃者。', '真、真', '偽、偽', '真、偽', '偽、真', 'A']

最初の問題のデータ:
列0: MITのケルベロスKDCサーバでは、(ほとんどのユーザプリンシパルに対して)チケットの最大存続時間は24時間である。期限切れのケルベロスチケットが使用できなくなることを保証するものは何か?
列1: ケルベロスサーバ(KDC)は、期限切れのチケットに対して、クライアントとサーバ間の新しい接続の確立を拒否する。
列2: クライアントがサーバに接続すると、サーバは接続を終了するために24時間のタイマーを設定し、これにより、チケットの最大有効期間を超えてクライアントが接続を維持できなくなる。
列3: クライアントがサーバに接続すると、サーバはチケットの有効期限をサーバの現在のクロックと比較し、チケットの有効期限が過ぎている場合はユーザの認証を拒否する。
列4: クライアントがサーバに接続すると、サーバはKDCにクエリを送信して、チケットがKDCのクロックに対してまだ有効であるかどうかをチェックし、KDCがチケットの期限切れを報告した場合は、ユーザの認証を拒否する。
列5: C

評価開始 - 全99問のコンピュータセキュリティ問題
Evaluating: 100%
 98/98 [00:54<00:00,  1.97it/s]
進捗: 25/99問完了、現在の正解率: 1/25 (0.0400)
進捗: 50/99問完了、現在の正解率: 4/50 (0.0800)
進捗: 75/99問完了、現在の正解率: 7/75 (0.0933)

評価完了！
モデル: elyza/ELYZA-japanese-Llama-2-7b
データセット: JMMLU computer_security
正解数: 7/98問
正解率: 0.0714 (7.14%)
"""