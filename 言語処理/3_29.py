import re
import json
import gzip
import requests

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

# 国旗画像のURLを取得する関数
def function(text):
    # 基礎情報を抽出
    info_dict = extract_basic_info(text)
    
    if '国旗画像' in info_dict:
        flag_image = info_dict['国旗画像']
        # ファイル名だけを抽出（余分なマークアップを除去）
        flag_image = re.sub(r'\[\[ファイル:|\[\[File:|]]', '', flag_image)
        flag_image = re.sub(r'\|.*$', '', flag_image)
        
        # MediaWiki APIを使用して画像URLを取得
        url = 'https://ja.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'imageinfo',
            'iiprop': 'url',
            'titles': f'File:{flag_image}'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # APIレスポンスから画像URLを抽出
        pages = data['query']['pages']
        for page_id in pages:
            if 'imageinfo' in pages[page_id]:
                return pages[page_id]['imageinfo'][0]['url']
    
    return None

print(function(load_uk_article()))