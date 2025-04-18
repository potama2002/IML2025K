import re
from typing import List
from knock20 import find_key_in_dictlist

def extract_media_files(article_text: str) -> List[str]:
    """
    記事本文からメディアファイル名を抽出する関数
    本文1つに対して実行する

    Args:
        article_text (str): 記事本文

    Returns:
        List[str]: メディアファイル名のリスト
    """
    pattern = r'\[\[(?:ファイル|File):([^|\]]+)'  # [[ファイル:◯◯|...]]または[[File:◯◯]]
    files = re.findall(pattern, article_text)
    return files

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} のメディアファイル一覧 ---")
        media_files = extract_media_files(article)
        for filename in media_files:
            print(filename)
        print("\n")
