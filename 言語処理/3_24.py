import re
import json
import gzip

def load_uk_article():
    with gzip.open('jawiki-country.json.gz','rt',encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']
    return None

#print(load_uk_article())
#3.21.py
def function(text):
    # [[ファイル:...]] または [[File:...]] 形式のパターン
    pattern = r'\[\[(ファイル|File):([^]|]+)(?:\|[^]]+)?\]\]'
    return [match.group(2) for match in re.finditer(pattern, text)]
print(function(load_uk_article()))