import re
import gzip
import json

def extract_uk_article(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data.get('title') == 'イギリス':
                return data.get('text')

file_path = 'jawiki-country.json.gz'
uk_text = extract_uk_article(file_path)

def extract_category_names(text):
    return re.findall(r'\[\[Category:(.*?)(?:\|.*)?\]\]', text)

print(extract_category_names)