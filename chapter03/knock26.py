import json
import gzip
import re

def load_uk():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for line in file:
            article = json.loads(line)
            if article['title'] == 'イギリス':
                return article['text']

def extract_template():
    data = re.search(r'\{\{基礎情報.*?\n\}\}', load_uk(), re.DOTALL).group()
    tuples = re.findall(r'\n\|(.+?)\s*=\s*(.+?)(?=(?:\n\||\n\}\}))', data, re.DOTALL)
    return dict(tuples)

def remove_emphases():
    d = extract_template()
    return {key: re.sub(r"'{2,5}", '', val) for key, val in d.items()}

# 結果を表示してみる
cleaned = remove_emphases()
for k, v in cleaned.items():
    print(f'{k}: {v}\n')
