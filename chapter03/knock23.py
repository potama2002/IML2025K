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

def extract_sections(text):
    sections = re.findall(r'^(={2,})\s*(.*?)\s*\1$', text, flags=re.MULTILINE)
    return [(sec, len(level) - 1) for level, sec in sections]

print(extract_sections)