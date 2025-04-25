import json
import re
import pandas as pd
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
import math
from knock37 import remove_mark_ups

if __name__ == "__main__":
    filename = "jawiki-country.json"
    j_data = pd.read_json(filename, lines=True)
    df = j_data
    jp_df = df[df["title"]=="日本"]
    jp_df = jp_df["text"].values
    mecab = MeCab.Tagger("-Ochasen")
    all_words = []
    # print(jp_df)

    dic = {}
    cleaned_text = ""
    for line in jp_df[0].split("\n"):
            # 基本情報の抽出
            if re.search("\|(.+?)\s=\s*(.+)", line):
                match_txt = re.search("\|(.+?)\s=\s*(.+)", line)
                dic[match_txt[1]] = match_txt[2]

            # 各種マークアップの除去処理
            match_sub = line
            match_sub = remove_mark_ups(match_sub)
            cleaned_text += match_sub + "\n"

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

    word_counts = Counter(all_words)
    total_words = sum(word_counts.values())  # 総単語数

    # TF (Term Frequency) の計算
    tf_dict = {}
    for word, count in word_counts.items():
        tf_dict[word] = count / total_words

    # 文書を段落に分割（簡易的なアプローチ）
    paragraphs = cleaned_text.split('\n\n')
    paragraphs = [p for p in paragraphs if p.strip()]  # 空の段落を除外

    # 各段落での単語の出現をカウント
    paragraph_word_sets = []
    for paragraph in paragraphs:
        node = mecab.parseToNode(paragraph)
        paragraph_words = set()
        
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
                        paragraph_words.add(word)
            node = node.next
        
        paragraph_word_sets.append(paragraph_words)

    # IDFの計算
    idf_dict = {}
    num_paragraphs = len(paragraph_word_sets)
    for word in word_counts.keys():
        # その単語を含む段落数をカウント
        doc_count = sum(1 for word_set in paragraph_word_sets if word in word_set)
        # IDFの計算（単語が1つも出現しない場合の対策として+1を加える）
        idf_dict[word] = math.log(num_paragraphs / (doc_count + 1)) + 1

    # TF-IDFスコアの計算
    tfidf_dict = {}
    for word in word_counts.keys():
        tfidf_dict[word] = tf_dict[word] * idf_dict[word]

    print("単語の総数:", total_words)
    print("ユニーク単語数:", len(word_counts))

    # 結果の表示（上位20語）
    print("\n日本の記事における名詞のTF・IDFスコア上位20語:")
    print("-" * 60)
    print(f"{'単語':<15} {'TF':<10} {'IDF':<10} {'TF-IDF':<10}")
    print("-" * 60)

    # TF-IDFスコア上位20語を抽出
    top_tfidf = sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)[:20]
    for word, tfidf_value in top_tfidf:
        print(f"{word:<15} {tf_dict[word]:<10.6f} {idf_dict[word]:<10.6f} {tfidf_value:<10.6f}")

"""
単語の総数: 23147
ユニーク単語数: 5574

日本の記事における名詞のTF・IDFスコア上位20語:
------------------------------------------------------------
単語              TF         IDF        TF-IDF    
------------------------------------------------------------
日本              0.040610   1.472501   0.059798  
世界              0.007301   2.624514   0.019162  
関係              0.005962   2.774454   0.016541  
憲法              0.004709   3.356375   0.015805  
経済              0.005271   2.804307   0.014781  
地方              0.004018   3.559974   0.014303  
中国              0.004623   2.986628   0.013806  
地域              0.004191   3.004977   0.012593  
文化              0.003931   3.187299   0.012531  
問題              0.004018   3.102141   0.012464  
時代              0.003888   3.143814   0.012224  
政府              0.004104   2.968610   0.012184  
世紀              0.003586   3.232761   0.011592  
天皇              0.003197   3.559974   0.011381  
Cite            0.003327   3.383044   0.011254  
台湾              0.002549   3.949439   0.010067  
社会              0.003067   3.280389   0.010062  
条約              0.002765   3.592764   0.009934  
国家              0.003154   3.143814   0.009915  
"""