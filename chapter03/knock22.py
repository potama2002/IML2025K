import json
import gzip
import re  # ← これを忘れてた！

def load_uk():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']

def extract_categs():
    return re.findall(r'\[\[Category:(.*?)(\|.*)?\]\]', load_uk())

# カテゴリ名だけを抽出して1行ずつ表示
print(*[match[0] for match in extract_categs()], sep='\n')
