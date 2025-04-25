import re
import json
import gzip

def load_uk_article():
    with gzip.open('jawiki-country.json.gz', 'rt', encoding='utf-8') as file:
        for item in file:
            d = json.loads(item)
            if d['title'] == 'イギリス':
                return d['text']
    return None

# 基礎情報を抽出する関数
def extract_basic_info(text):
    pattern = r'{{基礎情報.*?\n(.*?)\n}}'
    match = re.search(pattern, text, re.DOTALL)
    if match is None:
        return {}
    
    result = {}
    for field in re.finditer(r'\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)|(?=\n}))', match.group(1), re.DOTALL):
        result[field.group(1).strip()] = field.group(2).strip()
    
    return result

# 強調マークアップを除去する関数 (問題26)
def remove_emphasis_markup(text):
    pattern = r"''+([^']*)''"
    return re.sub(pattern, r'\1', text)

# 内部リンクを除去する関数 (問題27)
def remove_internal_links(text):
    pattern = r'\[\[(?:[^|]*?\|)?(.*?)\]\]'
    return re.sub(pattern, r'\1', text)

# MediaWikiマークアップを除去する関数 (問題28)
def function(text):
    # 基礎情報を抽出
    basic_info = extract_basic_info(text)
    
    # 各フィールドのマークアップを除去
    result = {}
    for field, value in basic_info.items():
        # 強調マークアップの除去
        value = remove_emphasis_markup(value)
        
        # 内部リンクの除去
        value = remove_internal_links(value)
        
        # 外部リンクの除去
        value = re.sub(r'\[https?://[\w./]*\s*(.*?)\]', r'\1', value)
        
        # HTMLタグの除去
        value = re.sub(r'<.*?>', '', value)
        
        # テンプレートの除去 ({{lang|en|...}} など)
        value = re.sub(r'{{(?:lang|仮リンク)(?:[^}])*?}}', '', value)
        
        # 残りのマークアップを除去
        value = re.sub(r'{{.+?}}', '', value)
        
        result[field] = value
    
    return result

print(function(load_uk_article()))