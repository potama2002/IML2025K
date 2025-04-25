import json
import re
import pandas as pd
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
# import japanize_matplotlib  # 日本語表示のため


def remove_mark_ups(match_sub):
    match_sub = re.sub("\'{2,}(.+?)\'{2,}", r"\1", match_sub)  # 強調マークアップ
    match_sub = re.sub(r'https?://\S+|www\.\S+', '', match_sub)
    match_sub = re.sub(r'=+([^=]+)=+', r'\1', match_sub)
    match_sub = re.sub(r'\[\[ファイル:([^\]\|]*)\]\]s', r'\1', match_sub)
    match_sub = re.sub(r"\[\[(.+?)\]\]", r"\1", match_sub)  # 内部リンク
    match_sub = re.sub(r"\[(.+?)\]", r"\1", match_sub)  # 外部リンク
    match_sub = re.sub(r"\*{1,}(.+?)", r"\1", match_sub)  # *箇条書き
    match_sub = re.sub(r"{{2,}(.+?)\}{2,}", r"\1", match_sub)  # {{}}で囲まれたもの
    match_sub = re.sub(r"\:(.+?)", r"\1", match_sub)  # コロン
    match_sub = re.sub(r'<.*?>', '', match_sub)  # HTMLタグ除去
    match_sub = re.sub(r'\{\{.*?\}\}', '', match_sub)  # テンプレート除去
    match_sub = re.sub(r'\[.*?\]', '', match_sub)  # 外部リンク除去
    match_sub = re.sub(r'\'+', '', match_sub)  # 残ったシングルクォート除去
    match_sub = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', match_sub)  # 内部リンクの表示名部分を取得
    match_sub = re.sub(r"('{2,5})(.+?)\1", r'\2', match_sub)  # 強調マークアップの別形式

    # グラフの削除
    match_sub = re.sub(r'\{\| .*?\n', '', match_sub)
    match_sub = re.sub(r'\|\}', '', match_sub)

    # テーブルヘッダー(!)とセパレーター(|-)を削除
    match_sub = re.sub(r'\|-', '', match_sub)
    match_sub = re.sub(r'! .*?\n', '', match_sub)

    # セル区切り(|)を削除し、セルの内容だけを残す
    match_sub = re.sub(r'\| ', '', match_sub)
    match_sub = re.sub(r'\|', '', match_sub)
    match_sub = re.sub(r'\{\{[^{}]*', '', match_sub)
    return match_sub

if __name__ == "__main__":
    filename = "jawiki-country.json"
    j_data = pd.read_json(filename, lines=True)
    df = j_data

    text_df = df["text"].values
    # print("データの件数:", len(text_df))
    
    mecab = MeCab.Tagger("-Ochasen")
    all_words = []

    # 全てのエントリに対して処理を行う
    for index, text in enumerate(text_df):
        dic = {}  # 各テキストごとに辞書を初期化
        cleaned_text = "" 
        
        # テキストを行ごとに処理
        for line in text.split("\n"):
            # 基本情報の抽出
            if re.search("\|(.+?)\s=\s*(.+)", line):
                match_txt = re.search("\|(.+?)\s=\s*(.+)", line)
                dic[match_txt[1]] = match_txt[2]
            
            # 各種マークアップの除去処理
            match_sub = line
            match_sub = remove_mark_ups(match_sub)
            cleaned_text += match_sub + "\n"
        # print(cleaned_text)
        
        node = mecab.parseToNode(cleaned_text)
        
        while node:
            features = node.feature.split(',')
            if features[0] in ['名詞']:  # 名詞
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
    print("\n===== 高頻度名詞TOP20 =====")
    for word, count in word_counts.most_common(20):
        print(f"{word}: {count}回")





"""
===== 高頻度名詞TOP20 =====
世界: 4623回
日本: 4341回
大統領: 3879回
of: 3803回
政府: 3536回
共和: 3222回
経済: 3039回
人口: 2833回
独立: 2685回
国際: 2683回
ファイル: 2613回
GDP: 2566回
国民: 2379回
国家: 2360回
イギリス: 2312回
フランス: 2243回
date: 2133回
地域: 2116回
文化: 2103回
首相: 2095回
"""