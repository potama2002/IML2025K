import json
import re
import pandas as pd
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
# import japanize_matplotlib  # 日本語表示のため

filename = "jawiki-country.json"
j_data = pd.read_json(filename, lines=True)
df = j_data

text_df = df["text"].values
mecab = MeCab.Tagger("-Ochasen")
all_words = []

# URLを削除する関数
def remove_url(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

# ウィキテーブルから文字部分のみを抽出する関数
def extract_table_content(text):
    # テーブル開始と終了の行は削除
    text = re.sub(r'\{\| .*?\n', '', text)
    text = re.sub(r'\|\}', '', text)

    # テーブルヘッダー(!)とセパレーター(|-)を削除
    text = re.sub(r'\|-', '', text)
    text = re.sub(r'! .*?\n', '', text)

    # セル区切り(|)を削除し、セルの内容だけを残す
    text = re.sub(r'\| ', '', text)
    text = re.sub(r'\|', '', text)

    return text

# 全てのエントリに対して処理を行う
for index, text in enumerate(text_df):
    # print(f"\n===== テキスト {index+1} の処理 =====")
    
    dic = {}  # 各テキストごとに辞書を初期化
    cleaned_text = ""

    
    # テキストを行ごとに処理
    for line in text.split("\n"):
        # 基本情報の抽出
        if re.search("\|(.+?)\s=\s*(.+)", line):
            match_txt = re.search("\|(.+?)\s=\s*(.+)", line)
            dic[match_txt[1]] = match_txt[2]
        line = remove_url(line)
        
        # 各種マークアップの除去処理
        match_sub = line
        match_sub = re.sub("\'{2,}(.+?)\'{2,}", r"\1", match_sub)  # 強調マークアップ
        match_sub = re.sub(r'=+([^=]+)=+', r'\1', match_sub)
        match_sub = re.sub(r'\[\[ファイル:([^\]\|]*)', r'\1', match_sub)
        match_sub = re.sub("\[\[(.+?)\]\]", r"\1", match_sub)  # 内部リンク
        match_sub = re.sub("\[(.+?)\]", r"\1", match_sub)  # 外部リンク
        match_sub = re.sub("\*{1,}(.+?)", r"\1", match_sub)  # *箇条書き
        match_sub = re.sub("{{2,}(.+?)\}{2,}", r"\1", match_sub)  # {{}}で囲まれたもの
        match_sub = re.sub("\:(.+?)", r"\1", match_sub)  # コロン
        match_sub = re.sub(r'<.*?>', '', match_sub)  # HTMLタグ除去
        match_sub = re.sub(r'\{\{.*?\}\}', '', match_sub)  # テンプレート除去
        match_sub = re.sub(r'\[.*?\]', '', match_sub)  # 外部リンク除去
        match_sub = re.sub(r'\'+', '', match_sub)  # 残ったシングルクォート除去
        match_sub = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', match_sub)  # 内部リンクの表示名部分を取得
        match_sub = re.sub(r"('{2,5})(.+?)\1", r'\2', match_sub)  # 強調マークアップの別形式
        
        
        cleaned_text += match_sub + "\n"
    table_pattern = r'\{\| class="wikitable".*?\|\}'
    tables = re.findall(table_pattern, text, re.DOTALL)
    
    for table in tables:
        # テーブルから文字部分のみを抽出
        extracted_content = extract_table_content(table)
        print("テーブルから抽出した内容:")
        print(extracted_content)
        cleaned_text += extracted_content + "\n"

    node = mecab.parseToNode(cleaned_text)
    
    while node:
        features = node.feature.split(',')
        if features[0] in ['名詞', '動詞', '形容詞']:  # 名詞、動詞、形容詞のみを対象
            if len(node.surface) > 1:  # 1文字の単語は除外
                if features[0] == '名詞' and features[1] in ['代名詞', '非自立', '数']:
                    # 代名詞、非自立名詞、数詞は除外
                    pass
                else:
                    # 基本形があれば基本形を使用、なければ表層形を使用
                    word = features[6] if len(features) > 7 and features[6] != '*' else node.surface
                    all_words.append(word)
        node = node.next


# 単語の頻度をカウント
word_counts = Counter(all_words)

# 頻度の高い順に20個の単語を出力
print("\n===== 高頻度単語TOP20 =====")
for word, count in word_counts.most_common(20):
    print(f"{word}: {count}回")


# """
# ===== 高頻度単語TOP20 =====
# いる: 13441回
# する: 9780回
# //: 8702回
# なる: 7519回
# ||: 6328回
# www: 5983回
# ある: 5756回
# en: 5453回
# 世界: 4694回
# of: 4534回
# れる: 4396回
# 日本: 4301回
# リンク: 4268回
# 大統領: 3975回
# )|: 3964回
# http: 3721回
# 政府: 3635回
# |-: 3343回
# 共和: 3295回
# jp: 3243回
# """
