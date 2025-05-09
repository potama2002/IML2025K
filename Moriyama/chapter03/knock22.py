import gzip
import json
import re

# 20: イギリスの記事を抽出
file_path = '/Users/takeru/Desktop/src‘ę3¸Ķbuk/Moriyama/chapter03/jawiki-country.json.gz'

uk_text = ''
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            uk_text = article['text'] # イギリス記事の本文（text）を uk_text に保存。
            break


# 22: カテゴリ名の抽出

for line in uk_text.split('\n'):
    match = re.search(r'\[\[Category:(.*?)(\|.*)?\]\]', line)
    if match:
        print(match.group(1))

"""
if match:
re.search(...) がマッチした場合は match にマッチオブジェクトが入る。

マッチしなかったら None になる。

つまり「カテゴリを含む行」だけを処理対象とするための条件分岐。


.group(1) → (.*?) でマッチした文字列だけを抽出。

"""