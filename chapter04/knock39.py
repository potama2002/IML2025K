import json
import re
import pandas as pd
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
# import japanize_matplotlib  # 日本語表示のため
import numpy as np
from knock37 import remove_mark_ups  # remove_mark_upsをknock37からインポート

if __name__ == "__main__":
    filename = "jawiki-country.json"
    j_data = pd.read_json(filename, lines=True)
    df = j_data

    text_df = df["text"].values
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
            match_sub = remove_mark_ups(match_sub)  # knock37からインポートした関数を使用
            cleaned_text += match_sub + "\n"

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

    # 単語の出現頻度を取得し、順位付け
    word_freq = [(word, count) for word, count in word_counts.items()]
    word_freq.sort(key=lambda x: x[1], reverse=True)  # 頻度の高い順にソート
    
    # 順位と頻度のリストを作成
    # # 順位と頻度のリストを作成
    # ranks = np.arange(1, len(word_freq) + 1)
    # words = [word for word, _ in word_freq]
    # frequencies = [freq for _, freq in word_freq]
    
    # # 両対数グラフをプロット
    # plt.figure(figsize=(12, 8))
    # plt.loglog(ranks, frequencies, 'bo', markersize=2, alpha=0.5)
    # plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # # トップ30単語にラベルを付ける
    # top_n = 30
    # for i in range(top_n):
    #     if i < len(word_freq):
    #         plt.annotate(
    #             words[i],
    #             xy=(ranks[i], frequencies[i]),
    #             xytext=(5, 0),
    #             textcoords='offset points',
    #             fontsize=8,
    #             alpha=0.8
    #         )
    
    # # グラフのタイトルと軸ラベルを設定
    # plt.title('単語出現頻度の順位-頻度分布（両対数）')
    # plt.xlabel('出現頻度順位')
    # plt.ylabel('出現頻度')
    
    # # ジップの法則を示す理論曲線を追加（参考用）
    # k = frequencies[0]  # 最も頻度の高い単語の頻度
    # zipf = [k/r for r in ranks]  # ジップの法則による理論値: f ∝ 1/r
    # plt.loglog(ranks, zipf, 'r-', alpha=0.7, label='Zipfの法則 (理論値)')
    
    # plt.legend()
    # plt.tight_layout()
    
    # # もし日本語表示が崩れる場合は、japanize_matplotlibをインポートするか
    # # 以下のように日本語フォントを設定する
    # # plt.rcParams['font.family'] = 'MS Gothic'  # Windows
    # plt.rcParams['font.family'] = 'Hiragino Sans GB'  # Mac
    # # plt.rcParams['font.family'] = 'IPAGothic'  # Linux
    
    # plt.savefig('word_freq_rank.png', dpi=300)
    # plt.show()
    ranks = np.arange(1, len(word_freq) + 1)
    frequencies = [freq for _, freq in word_freq]
    
    # 両対数グラフをプロット
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, 'bo', markersize=2, alpha=0.5)
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # グラフのタイトルと軸ラベルを設定
    plt.title('単語出現頻度の順位-頻度分布（両対数）')
    plt.xlabel('出現頻度順位')
    plt.ylabel('出現頻度')
    
    # ジップの法則を示す理論曲線を追加（参考用）
    k = frequencies[0]  # 最も頻度の高い単語の頻度
    zipf = [k/r for r in ranks]  # ジップの法則による理論値: f ∝ 1/r
    plt.loglog(ranks, zipf, 'r-', alpha=0.7, label='Zipfの法則 (理論値)')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('word_freq_rank.png')
    plt.show()