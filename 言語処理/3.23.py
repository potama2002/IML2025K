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

def function(text):
    pattern = r'(={2,})\s*(.+?)\s*\1'
    sections = []
    for match in re.finditer(pattern, text):
        level = len(match.group(1)) - 1  # セクションレベルを計算
        name = match.group(2)
        sections.append((level, name))
    return sections
print(function(load_uk_article()))