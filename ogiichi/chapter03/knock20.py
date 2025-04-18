import json

#jsonファイル読取関数
def read_wikipedia_article(filename, target_title):
    with open(filename, 'r', encoding='utf-8') as f:    #f：openfileのこと
        for line in f:
            # 各行をJSON形式の辞書オブジェクトにデコード
            article = json.loads(line)
            # タイトルがターゲットと一致する場合、記事本文を返す
            if article.get('title') == target_title:
                return article.get('text')
    return None

filename = 'jawiki-country.json'
target_title = 'イギリス'

text = read_wikipedia_article(filename, target_title)
if text:
    print(text)
else:
    print(f"記事 '{target_title}' が見つかりませんでした。")
