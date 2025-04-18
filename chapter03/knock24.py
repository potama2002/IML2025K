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


#　24 ファイル参照の抽出

pattern = r'\[\[(?:File|ファイル):(.+?\.(?:svg|jpg|jpeg|png|gif|tiff|tif|ogg|mp3|wav))'

# re.findall()
# 第1引数：パターン
# 第2引数：対象文字列
# 第3引数：フラグ（IGNORECASEで大文字小文字を区別しない）
# → マッチしたグループ（括弧で囲んだ部分）をリストとしてすべて返す
matches = re.findall(pattern, uk_text, re.IGNORECASE)

for filename in matches:
    print(filename)

      