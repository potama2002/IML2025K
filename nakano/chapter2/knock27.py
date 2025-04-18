import re
from typing import Dict
from knock20 import find_key_in_dictlist   
from knock25 import extract_basic_info     
from knock26 import remove_emphasis_markup 

def remove_internal_links(text: str) -> str:
    """
    MediaWikiの内部リンクマークアップを除去する関数

    Args:
        text (str): マークアップ付きテキスト

    Returns:
        str: 内部リンク除去後のテキスト
    """
    # [[記事名|表示名]] → 表示名
    #text = re.sub(r'\[\[(?:[^|\]]+\|)?([^|\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1',text)
    return text

def clean_basic_info_full(basic_info: Dict[str, str]) -> Dict[str, str]:
    """
    基礎情報辞書から強調マークアップと内部リンクを除去する関数

    Args:
        basic_info (Dict[str, str]): 基礎情報辞書（q25の結果）

    Returns:
        Dict[str, str]: マークアップ除去済みの基礎情報辞書
    """
    cleaned_info = {}
    for field, value in basic_info.items():
        value_no_emphasis = remove_emphasis_markup(value)   # 強調除去(q26)
        value_no_links = remove_internal_links(value_no_emphasis)  # 内部リンク除去
        cleaned_info[field] = value_no_links
    return cleaned_info

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} の基礎情報（強調マークアップ＋内部リンク除去後）---")
        basic_info = extract_basic_info(article)   # 基礎情報取得(q25)
        cleaned_info = clean_basic_info_full(basic_info)  # 強調＋内部リンク除去

        for field, value in cleaned_info.items():
            print(f"{field}: {value}")
        print("\n")
