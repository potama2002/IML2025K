# 43

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
   prompt = f"""以下のコンピュータセキュリティに関する多肢選択問題を注意深く考えて解いてください。
ステップバイステップで考え、各選択肢を分析してから最適な答えを選んでください。

問題: {question}

選択肢:
A. {choices[0]}
B. {choices[1]}
C. {choices[2]}
D. {choices[3]}

問題に関連する概念や定義を思い出し、各選択肢の妥当性を評価してください。
あなたの推論過程を示し、最後に「答え: X」の形式で回答を明確に示してください。ここでXはA、B、C、Dのいずれかです。
"""
   return prompt

def extract_answer(text):
   """モデルの出力から回答を抽出する関数"""
   # 明確な「答え: X」のフォーマットを最優先で検索
   pattern1 = r"答え\s*[:：]\s*([ABCD])"
   match1 = re.search(pattern1, text)
   if match1:
       return match1.group(1)

   # 文末の「したがって、答えはX」「よって、X」などのパターン
   pattern_conclusion = r"(?:したがって|よって|結論として|以上より)[^ABCD]*([ABCD])[^ABCD]*(?:が正解|を選択|が適切)"
   match_conclusion = re.search(pattern_conclusion, text)
   if match_conclusion:
       return match_conclusion.group(1)

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

   # テキスト全体からA,B,C,Dを探し、最後に言及されたものを優先
   choices = re.findall(r'\b[ABCD]\b', text)
   if choices:
       # 最後の5つの選択肢の中で最も頻出のものを返す（最終的な結論を重視）
       if len(choices) >= 5:
           recent_choices = choices[-5:]
           return max(set(recent_choices), key=recent_choices.count)
       return choices[-1]  # 最後に言及された選択肢

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
               temperature=0.0,  # 温度を0に変更
               do_sample=False,  # サンプリングをオフに
               top_p=1.0,        # トップP値を最大に
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
 98/98 [00:31<00:00,  3.22it/s]
/usr/local/lib/python3.11/dist-packages/transformers/generation/configuration_utils.py:631: UserWarning: `do_sample` is set to `False`. However, `temperature` is set to `0.0` -- this flag is only used in sample-based generation modes. You should set `do_sample=True` or unset `temperature`.
  warnings.warn(
進捗: 25/99問完了、現在の正解率: 0/25 (0.0000)
進捗: 50/99問完了、現在の正解率: 0/50 (0.0000)
進捗: 75/99問完了、現在の正解率: 0/75 (0.0000)

評価完了！
モデル: elyza/ELYZA-japanese-Llama-2-7b
データセット: JMMLU computer_security
正解数: 0/98問
正解率: 0.0000 (0.00%)
"""