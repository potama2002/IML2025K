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


# 23: セクション構造
for line in uk_text.split('\n'):
    match = re.match(r'(={2,})\s*(.+?)\s*\1', line)
    if match:
        level = len(match.group(1)) - 1
        title = match.group(2)
        print('{} (level {})'.format(title, level))

"""
(={2,})     → グループ1：「==」以上の `=` の連続（最低2個）
\s*         → 任意の空白（あってもなくてもOK）
(.+?)       → グループ2：セクション名（非貪欲）
\s*         → セクション名の後の空白も許容
\1          → 最初と同じ数の `=` で閉じる（グループ1と同じ）


"""