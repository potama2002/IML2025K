import re
from typing import List, Tuple
from knock20 import find_key_in_dictlist

def extract_sections(article_text: str):
    """
    記事本文からセクション名とそのレベルを抽出する関数
    本文1つに対して実行すること
    遅延評価を利用して、セクション名を1つずつ生成するジェネレータ関数

    Args:
        article_text (str): 記事本文

    Returns:
        Tuple[int, str]: セクション名とレベルのタプル
    """
    sections = []
    for line in article_text.split('\n'):
        # =の数とセクション名を抽出
        match = re.match(r'^(=+)\s*(.*?)\s*\1$', line)
        if match:
            level = len(match.group(1)) - 1  # "="の数 -1 がレベルに対応する
            section_name = match.group(2)
            yield level, section_name
            #sections.append((level, section_name))
    #return sections

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key) 
    articles =list(articles)
    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} のセクション一覧 ---")
        sections = extract_sections(article)
        for level, name in sections:
            print(f"レベル {level}: {name}")
        print("\n")
