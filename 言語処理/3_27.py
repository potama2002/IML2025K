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
    # [[記事名]] → 記事名
    # [[記事名|表示文字]] → 表示文字
    pattern = r'\[\[(?:[^|]*\|)?([^]]+)\]\]'
    return re.sub(pattern, r'\1', text)


print(function(load_uk_article()))