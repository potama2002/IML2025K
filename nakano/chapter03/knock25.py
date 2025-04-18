import re
from typing import Dict
from knock20 import find_key_in_dictlist  # q20からインポート

def extract_basic_info(article_text: str) -> Dict[str, str]:
    """
    「基礎情報 国」テンプレートのフィールド名と値を辞書にして返す関数

    Args:
        article_text (str): 記事本文

    Returns:
        Dict[str, str]: 基礎情報のフィールド名と値の辞書
    """
    # 基礎情報テンプレートを抽出（非貪欲マッチ）
    template_match = re.search(r'\{\{基礎情報 国(.*?)\n\}\}', article_text, re.DOTALL)
    if not template_match:
        return {}

    template_text = template_match.group(1)

    # フィールド名と値を抽出
    fields = {}
    field_pattern = r'\n\|(.+?)\s*=\s*(.+?)(?=\n\||\n$)'
    matches = re.findall(field_pattern, template_text, re.DOTALL)
    
    for field_name, value in matches:
        fields[field_name.strip()] = value.strip()

    return fields

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)  # q20.pyから記事を取得

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} の基礎情報 ---")
        basic_info = extract_basic_info(article)
        for field, value in basic_info.items():
            print(f"{field}: {value}")
        print("\n")
