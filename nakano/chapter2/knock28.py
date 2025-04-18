import re
from typing import Dict
from knock20 import find_key_in_dictlist
from knock25 import extract_basic_info
from knock26 import remove_emphasis_markup
from knock27 import remove_internal_links

def remove_markup(text: str) -> str:
    """
    MediaWikiマークアップを可能な限り除去する関数
    """
    text = remove_emphasis_markup(text)  # 強調除去
    text = remove_internal_links(text)   # 内部リンク除去
    text = re.sub(r'<.*?>', '', text)  # HTMLタグ除去
    text = re.sub(r'\{\{.*?\}\}', '', text)  # テンプレート除去
    text = re.sub(r'\[.*?\]', '', text)  # 外部リンク除去
    text = re.sub(r'\'+', '', text)  # 残ったシングルクォート除去
    return text.strip()

def fully_clean_basic_info(basic_info: Dict[str, str]) -> Dict[str, str]:
    """
    基礎情報辞書から全てのマークアップを除去する関数
    """
    cleaned_info = {}
    for field, value in basic_info.items():
        cleaned_info[field] = remove_markup(value)
    return cleaned_info

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} の基礎情報（完全マークアップ除去後）---")
        basic_info = extract_basic_info(article)
        cleaned_info = fully_clean_basic_info(basic_info)

        for field, value in cleaned_info.items():
            print(f"{field}: {value}")
        print("\n")
