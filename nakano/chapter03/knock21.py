import re
from typing import List

from knock20 import get_dictlist_from_json, find_key_in_dictlist


def extract_category_lines(article_text: str) -> List[str]:
    """
    記事本文からカテゴリ名を含む行を抽出する関数
    本文1つに対して実行すること

    Args:
        article_text (str): 1つの記事本文

    Returns:
        List[str]: カテゴリ行だけを集めたリスト
    """
    lines = article_text.split('\n')  # 改行ごとに分割
    category_lines = [line for line in lines if re.search(r'\[\[Category:', line)]
    return category_lines

    
if __name__ == "__main__":

    filepath =  'json/jawiki-country.json'
    target_title = 'イギリス'

    articles = find_key_in_dictlist(filepath, target_title)

    # 各記事についてカテゴリ行を抽出して表示
    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} のカテゴリ行 ---")
        category_lines = extract_category_lines(article)
        for line in category_lines:
            print(line)
        print("\n")