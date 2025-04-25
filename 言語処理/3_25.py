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
    # 基礎情報部分を抽出
    pattern = r'{{基礎情報[^}]*\n(.*?)\n}}'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return {}
    
    template_text = match.group(1)
    
    # フィールド名と値を抽出
    field_pattern = r'\|([^=]+)=\s*(.+?)(?=\n\||\n$)'
    fields = re.findall(field_pattern, template_text, re.DOTALL)
    
    info_dict = {}
    for name, value in fields:
        # 前後の空白を除去
        name = name.strip()
        value = value.strip()
        info_dict[name] = value
    
    return info_dict

print(function(load_uk_article()))