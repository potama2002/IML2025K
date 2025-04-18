import json
import gzip
import re

def load_uk():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']

def extract_media_files():
    # [[File:○○|...]] または [[ファイル:○○|...]] をマッチ
    return re.findall(r'\[\[(?:File|ファイル):(.+?)(?:\|.*)?\]\]', load_uk())

# 出力（1行ずつ）
for filename in extract_media_files():
    print(filename)
