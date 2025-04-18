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

def clean_markup(value):
    value = remove_emphasis_markup(value)
    value = remove_internal_links(value)
    value = re.sub(r'<.*?>', '', value)  # HTMLタグ
    value = re.sub(r'\[http[^\s\]]+(\s(.+?))?\]', r'\2', value)  # 外部リンク
    value = re.sub(r'\{\{.*?\}\}', '', value)  # テンプレート
    value = re.sub(r'\[.*?\]', '', value)  # 残りの角括弧リンクなど
    return value.strip()