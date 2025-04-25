import json
import gzip

def load_uk():
    with gzip.open('jawiki-country.json.gz','rt',encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)

            if d['title'] == 'イギリス':
                return d['text']

print(load_uk())
