import re
from typing import Dict
from knock20 import find_key_in_dictlist  
from knock25 import extract_basic_info    

def remove_emphasis_markup(text: str) -> str:
    """
    MediaWikiの強調マークアップを除去する関数

    Args:
        text (str): マークアップ付きテキスト

    Returns:
        str: マークアップ除去後のテキスト
    """
    # 強調マークアップ（斜体・太字）を除去
    return re.sub(r"('{2,5})(.+?)\1", r'\2', text)

def clean_basic_info(basic_info: Dict[str, str]) -> Dict[str, str]:
    """
    基礎情報辞書の値から強調マークアップを除去する関数

    Args:
        basic_info (Dict[str, str]): 基礎情報辞書（q25の結果）

    Returns:
        Dict[str, str]: 強調マークアップ除去済みの基礎情報辞書
    """
    cleaned_info = {}
    for field, value in basic_info.items():
        cleaned_value = remove_emphasis_markup(value)
        cleaned_info[field] = cleaned_value
    return cleaned_info

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} の基礎情報（強調マークアップ除去後）---")
        basic_info = extract_basic_info(article)   # 基礎情報を取得（q25）
        cleaned_info = clean_basic_info(basic_info)  # 強調マークアップ除去

        for field, value in cleaned_info.items():
            print(f"{field}: {value}")
        print("\n")
