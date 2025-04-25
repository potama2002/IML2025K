import MeCab                               # 日本語形態素解析器MeCabを使う
import gzip                                # .gzファイルを開くため
import json                                # JSON形式の読み込み
import re                                  # テキストの前処理（記号削除）に使用
import math                                # 対数計算（IDF計算）に使用
from collections import Counter, defaultdict  # 単語の頻度を数える辞書型ツール

# MeCabのTaggerオブジェクトを作成（デフォルトは mecab-ipadic）
tagger = MeCab.Tagger()

# 各文書における単語の出現回数を集計（日本に関する記事のTF用）
target_tf = Counter()

# 各単語が何文書に現れたかを数える（DF）
df_counter = Counter()

# 全文書数（N）をカウント
N = 0

# Wikipediaコーパスのパス（要修正：自分のファイルに合わせて）
file_path = "/Users/takerumoriyama/Downloads/jawiki-country.json.gz"

# 圧縮されたWikipediaファイルを1行ずつ読み込む
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        N += 1  # 文書数をカウント

        # 1行（=1記事）をJSONとしてパース
        article = json.loads(line)
        title = article.get("title", "")
        text = article.get("text", "")

        # Wikipedia構文の簡易除去（正規表現で記号をスペースに）
        text = re.sub(r"[{}\[\]|=<>:/\*#]+", " ", text)
        text = text.replace("ref", "").replace("br", "")

        # この文書で一度でも出現した単語を記録するためのセット
        appeared_words = set()
        # この文書内での名詞の出現回数をカウント
        tf_local = Counter()

        # MeCabで形態素解析
        parsed = tagger.parse(text)
        for line in parsed.split("\n"):
            if "\t" not in line:
                continue  # EOSや空行などはスキップ

            surface, feature = line.split("\t")
            features = feature.split(",")
            pos = features[0]                          # 品詞（名詞、動詞など）
            lemma = features[6] if len(features) > 6 else surface  # 原形（辞書形）

            # 名詞のみ対象にし、空白・*（不明語）を除外
            if pos == "名詞" and lemma != "*" and lemma.strip():
                tf_local[lemma] += 1                   # この文書内でのTF加算
                appeared_words.add(lemma)              # DF集計用セットに追加

        # DFを更新：その文書で出現したすべての単語についてカウント+1
        for word in appeared_words:
            df_counter[word] += 1

        # 文書タイトルに「日本」が含まれていたら、TFをグローバルに統合
        if "日本" in title:
            target_tf.update(tf_local)

# TF-IDFのスコア計算結果を格納するリスト
results = []

# TFのある単語ごとに、TF-IDFを計算
for word, tf in target_tf.items():
    df = df_counter[word]                # その単語の出現文書数
    idf = math.log(N / (1 + df))         # IDF計算（log(N / df)、+1でゼロ割防止）
    tf_idf = tf * idf                    # TF × IDF
    results.append((word, tf, df, idf, tf_idf))

# TF-IDFスコアで降順ソート
results.sort(key=lambda x: x[4], reverse=True)

# 上位20語を表示
print("単語\tTF\tDF\tIDF\tTF-IDF")
for word, tf, df, idf, tf_idf in results[:20]:
    print(f"{word}\t{tf}\t{df}\t{round(idf, 4)}\t{round(tf_idf, 2)}")


""" 実行結果
単語    TF      DF      IDF     TF-IDF
琉球    50      3       4.1271  206.36
天皇    78      18      2.569   200.38
倭      46      4       3.904   179.58
倭国    40      2       4.4148  176.59
沖縄    55      17      2.6231  144.27
朝鮮    56      18      2.569   143.86
列島    43      11      3.0285  130.23
日本書紀        27      1       4.8203  130.15
日本    984     221     0.1108  108.98
所蔵    26      4       3.904   101.5
韓国    64      51      1.5622  99.98
県      191     146     0.523   99.89
明治    40      20      2.4689  98.76
台湾    65      54      1.5061  97.9
北海道  39      21      2.4224  94.47
唐      30      10      3.1155  93.47
北陸    19      1       4.8203  91.59
アイヌ  20      2       4.4148  88.3
九州大学        20      2       4.4148  88.3
政令    29      11      3.0285  87.83
"""