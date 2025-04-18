import json
import gzip
import re

def load_uk():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']

def extract_categ_lines():
    return re.findall(r'.*Category.*', load_uk())

print(*extract_categ_lines(), sep='\n')  # 各行を改行して表示
