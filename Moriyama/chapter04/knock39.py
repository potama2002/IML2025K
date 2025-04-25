import MeCab  # 日本語の形態素解析ライブラリ（品詞分解・原形化などが可能）
import gzip   # .gz 圧縮ファイルを直接開くための標準ライブラリ
import json   # JSON形式（1記事1行）をPython辞書として読み込む
import re     # 正規表現ライブラリ（記号やタグの除去に使用）
from collections import Counter  # 単語の出現回数を簡単にカウントできる辞書
import matplotlib.pyplot as plt  # グラフ描画ライブラリ（今回は出現頻度グラフ）

# MeCabの解析器オブジェクトを作成
tagger = MeCab.Tagger()

# 単語の出現回数を数えるためのCounterオブジェクト
counter = Counter()

# Wikipediaの圧縮済みJSONファイルのパスを指定
file_path = "/Users/takerumoriyama/Downloads/jawiki-country.json.gz"

# 圧縮ファイルを開いて、1行（＝1記事）ずつ処理する
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        # 1行のJSONを辞書として読み込む
        article = json.loads(line)

        # 本文のテキストだけを取り出す（titleではなくtext）
        text = article.get("text", "")

        # Wikipediaの構文などを除去（簡易的に正規表現と置換）
        text = re.sub(r"[{}\[\]|=<>:/\*#]+", " ", text)
        text = text.replace("ref", "").replace("br", "")

        # MeCabでテキストを形態素解析（返り値は文字列）
        parsed = tagger.parse(text)

        # 各単語ごとに1行で分割しながら解析結果を処理
        for line in parsed.split("\n"):
            if "\t" not in line:
                continue  # EOS（終端）や空行などはスキップ

            # 「表層形」と「形態素情報」に分ける
            surface, feature = line.split("\t")
            features = feature.split(",")

            # 原形（lemma）：第7フィールドに原形が入っている
            lemma = features[6] if len(features) > 6 else surface

            # 無効な原形（例：* や 空）を除外
            if lemma != "*" and lemma.strip():
                counter[lemma] += 1  # カウントを加算
# 出現頻度が高い順に単語を並べる（most_common は自動でソート済み）
word_freq = counter.most_common()

# 単語の出現順位を1から順に付ける（1位, 2位, ..., N位）
ranks = range(1, len(word_freq) + 1)

# 単語の出現頻度リストを抽出（グラフのY軸用）
frequencies = [freq for _, freq in word_freq]

# グラフを作成（サイズを指定）
plt.figure(figsize=(8, 6))

# 順位（X軸）と出現頻度（Y軸）の関係を折れ線グラフで描く
plt.plot(ranks, frequencies)

# 両軸とも対数スケールにする（Zipfの法則を確認するため）
plt.xscale('log')
plt.yscale('log')

# 軸ラベルやタイトルの設定
plt.xlabel("順位（Rank）")
plt.ylabel("出現頻度（Frequency）")
plt.title("Zipfの法則：単語の出現頻度と順位の両対数グラフ")

# グリッド（補助線）を表示
plt.grid(True)

# レイアウトを最適化して、はみ出しを防止
plt.tight_layout()

# グラフを表示（※ターミナルでは表示されない場合があるので注意）
plt.show()
