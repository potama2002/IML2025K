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
    # 基礎情報テンプレート全体を抽出
    data = re.search(r'\{\{基礎情報.*?\n\}\}', load_uk(), re.DOTALL).group()
    
    # 各フィールドを(key, value)に分割
    tuples = re.findall(r'\n\|(.+?)\s*=\s*(.+?)(?=(?:\n\||\n\}\}))', data, re.DOTALL)
    
    return dict(tuples)

# 結果を表示
for k, v in extract_template().items():
    print(f'{k}: {v}\n')
