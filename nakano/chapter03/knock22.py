# カテゴリを含む行ではなく，カテゴリのみを抽出する
# 

import re
from typing import List

from knock20 import get_dictlist_from_json, find_key_in_dictlist


def extract_category_names(article_text: str) -> List[str]:
    """
    記事本文からカテゴリ名を抽出する関数
    これも本文1つに対して実行すること

    Args:
        article_text (str): 1つの記事本文

    Returns:
        List[str]: カテゴリ名（文字列）のリスト
    """
    lines = article_text.split('\n')
    category_names = []
    for line in lines:
        
        match = re.search(r'\[\[Category:(.*?)(\|.*)?\]\]', line)
        if match:
            category_name = match.group(1)  # 1番目のグループがカテゴリ名
            category_names.append(category_name)
    return category_names


if __name__ == "__main__":
    filepath =  'json/jawiki-country.json'
    target_title = 'イギリス'

    # タイトルがイギリスの記事を取得
    articles:list[str] = find_key_in_dictlist(filepath, target_title)
    

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} のカテゴリ名 ---")
        category_names = extract_category_names(article)
        for name in category_names:
            print(name)
        print("\n")

'''出力
(nlp_100knock) nkn4ryu@nkn4ryu-pro chapter03 % python knock22.py 
--- 記事 1 のカテゴリ名 ---
イギリス領ヴァージン諸島
カリブ海の諸島
欧州連合加盟国の特別領域


--- 記事 2 のカテゴリ名 ---
イギリス領インド洋地域
インド洋の島
イギリスの海外領土
欧州連合加盟国の特別領域
1965年に成立した国家・領域


--- 記事 3 のカテゴリ名 ---
イギリス
イギリス連邦加盟国
英連邦王国
G8加盟国
欧州連合加盟国
海洋国家
現存する君主国
島国
1801年に成立した国家・領域



'''