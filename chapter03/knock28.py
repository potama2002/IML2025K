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

def remove_links():
    d = remove_emphases()
    return {key: re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', val) for key, val in d.items()}

def remove_markups():
    d = remove_links()
    # 外部リンクの表示名のみを残す
    d = {key: re.sub(r'\[http[^\s]*\s(.+?)\]', r'\1', val) for key, val in d.items()}
    # ref や br タグの除去
    d = {key: re.sub(r'</?(ref|br)[^>]*?>', '', val) for key, val in d.items()}
    return d

# 出力確認
for k, v in remove_markups().items():
    print(f'{k}: {v}\n')
