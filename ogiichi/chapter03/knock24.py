import json
import re

#jsonファイル読取関数
def read_wikipedia_article(filename, target_title):
    with open(filename, 'r', encoding='utf-8') as f:
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

# メディアファイルを抽出する正規表現パターン
'''
このパターンは、テキストの中から「[[ファイル:～]]」という形をした部分を探し出し、その中からファイル名だけを取り出すため
'''
pattern_media = r'\[\[ファイル:(.+?)(?:\|.*?)?\]\]'

# メディアファイル名を抽出
'''
re.findall：正規表現に一致する全ての部分をリストで返す
'''
media_files = re.findall(pattern_media, text)

# メディアファイル名を出力
if media_files:
    print("参照されているメディアファイル:")
    for media in media_files:
        print(media)
else:
    print("メディアファイルが見つかりません")
