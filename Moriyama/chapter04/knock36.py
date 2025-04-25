import MeCab
import gzip
import json
import re
from collections import Counter

# MeCabオブジェクトの作成
tagger = MeCab.Tagger()
counter = Counter()

# 圧縮されたWikipediaデータのパス（自分の環境に合わせて）
file_path = "/Users/takerumoriyama/Downloads/jawiki-country.json.gz"

# gzipファイルを開いて1行ずつ処理（各行がWikipedia記事）
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for i, line in enumerate(f):
        

        article = json.loads(line)
        text = article.get("text", "")

        # Wikiマークアップや記号を削除（簡易的な前処理）
        text = re.sub(r"[{}\[\]|=<>:/\*#]+", " ", text)
        text = text.replace("ref", "").replace("br", "")

        # MeCabで形態素解析
        parsed = tagger.parse(text)

        # 各行を処理
        for line in parsed.split("\n"):
            if "\t" not in line:
                continue
            surface, feature = line.split("\t")
            features = feature.split(",")
            lemma = features[6] if len(features) > 6 else surface

            # 無効な原形（*など）はスキップ
            if lemma == "*" or not lemma.strip():
                continue

            # カウントに追加（品詞は問わない）
            counter[lemma] += 1

# 出現頻度の上位20語を表示
for word, freq in counter.most_common(20):
    print(f"{word}\t{freq}")

"""実行結果
の      97952
、      86699
。      53128
は      52377
に      50257
する    48079
が      44545
を      39317
た      35616
年      30225
と      28375
て      26019
だ      21785
で      21490
）      18987
（      18665
れる    18573
いる    17515
ある    17439
月      13705
"""