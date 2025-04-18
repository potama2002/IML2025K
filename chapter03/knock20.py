import gzip
import json

def extract_uk_article(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data.get('title') == 'イギリス':
                return data.get('text')

# ファイルパスを適宜指定
file_path = 'jawiki-country.json.gz'
uk_text = extract_uk_article(file_path)

# イギリスの記事本文を表示（長いので一部だけにする場合も）
print(uk_text[:1000])