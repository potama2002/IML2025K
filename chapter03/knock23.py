import json
import gzip
import re  # ← ここを忘れずに！

def load_uk():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']

def extract_sects():
    # セクション名と = の数を取得
    tuples = re.findall(r'(={2,})\s*([^\s=]+).*', load_uk())

    sects = []
    for t in tuples:
        level = len(t[0]) - 1  # = の数 - 1 が階層レベル
        sects.append([t[1], level])

    return sects

# 出力（1行ずつ表示）
for name, level in extract_sects():
    print(f'{name} (レベル{level})')
