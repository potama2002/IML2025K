import gzip
import json
import re

# 20: イギリスの記事を抽出
file_path = '/Users/takeru/Downloads/src‘ę3¸Ķ/Moriyama/chapter03/jawiki-country.json.gz'

uk_text = ''
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            uk_text = article['text'] # イギリス記事の本文（text）を uk_text に保存。
            break

# 21: [[Category:...]] を含む行を抽出
for line in uk_text.split('\n'):  #本文を改行（\n）で分割して、1行ごとに処理できるようにする。
    if re.search(r'\[\[Category:.*\]\]', line): #.は任意の一文字、＊は直前の要素を０回以上繰り返すという意味
        print(line)
"""
re.search(pattern, string)
Pythonの正規表現ライブラリ re の関数。

引数に 検索したいパターン と 対象の文字列 を与える。

マッチする部分がどこかにあればTrue、なければ None を返します。

r'' はバックスラッシュ（\）をエスケープシーケンスとして解釈せず、そのままの文字として扱うという意味

"""