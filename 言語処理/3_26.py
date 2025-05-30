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
    # 弱い強調、強調、強い強調を除去（''、'''、'''''）
    text = re.sub(r"''+", "", text)
    return text


print(function(load_uk_article()))