import MeCab                            # 日本語形態素解析エンジンMeCabのPythonバインディング
import gzip                             # .gz（gzip圧縮）ファイルを扱うための標準ライブラリ
import json                             # JSON形式のテキストを辞書に変換するために使用
import re                               # 文字列から記号などを除去するために使用
from collections import Counter         # 単語の出現回数を効率よく数えるための便利なクラス

# MeCabのTaggerオブジェクトを作成（mecab-ipadic辞書を使って構文解析）
tagger = MeCab.Tagger()

# 出現頻度を数えるためのCounterオブジェクトを作成（辞書型＋自動カウント）
counter = Counter()

# Wikipedia記事（JSON形式で1記事＝1行）の圧縮ファイルパスを指定
file_path = "/Users/takerumoriyama/Downloads/jawiki-country.json.gz"

# gzipファイルを開いて、1行ずつ読み込む（各行が1つのWikipedia記事）
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for i, line in enumerate(f):
        # i = 行番号（インデックス）だが、今回は途中で止めずに全記事を処理

        # 1行（＝1記事）を辞書型に変換
        article = json.loads(line)

        # 'text' キーにある本文だけを取得（記事タイトルは 'title' にある）
        text = article.get("text", "")

        # Wikipedia特有の構文（記号など）をざっくり正規表現で除去（前処理）
        text = re.sub(r"[{}\[\]|=<>:/\*#]+", " ", text)
        text = text.replace("ref", "").replace("br", "")

        # MeCabで形態素解析を実行（結果は文字列形式で返ってくる）
        parsed = tagger.parse(text)

        # MeCabの出力を1行ずつ処理（各行は1形態素）
        for line in parsed.split("\n"):
            if "\t" not in line:
                continue  # EOSや空行など解析対象でない行をスキップ

            # 「表層形（表示された単語）」と「形態素情報（品詞など）」に分割
            surface, feature = line.split("\t")
            features = feature.split(",")

            # 品詞の大分類（名詞・動詞・助詞…など）を取得（features[0]）
            pos = features[0]

            # 原形（辞書形）：存在しないときは "*" になる（features[6]）
            lemma = features[6] if len(features) > 6 else surface

            # 名詞かつ有効な原形（*や空文字は除外）だけをカウント
            if pos == "名詞" and lemma != "*" and lemma.strip():
                counter[lemma] += 1

# 出現頻度が高い単語トップ20を表示
for word, freq in counter.most_common(20):
    print(f"{word}\t{freq}")

""" 実行結果
年      30225
月      13705
日      10413
人      10142
国      9087
語      6061
的      5260
世界    4819
こと    4642
日本    4530
リンク  4414
大統領  4059
政府    3650
ため    3550
州      3444
島      3373
共和    3352
者      3320
経済    3228
人口    2964
"""