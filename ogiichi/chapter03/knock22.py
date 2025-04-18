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

#カテゴリ名を抽出する関数
def extract_category_names(text):
    '''
    \[\[Category:：「[[Category:」から始まり，「]]」で終わる文字列を探す
    (?P<categoryName>[^|\]]+)(?:\|[^]]+)：
        ()：「[[Category:」と「]]」の部分を省く→[[Category:〜]]の〜の部分のみを抽出する
        ?：非貪欲マッチ（最小マッチ）
        P<categoryName>：取り出した部分（〜の部分）に名前をつけている
        [^|\]：`Category:` に続く「`|` や `]` が来るまでの部分」を取り出す
        (?:\|[^]]+)?：
            (?:  )：この部分をグループ化して使うが，最終的には使用しないという設定
            |：続く部分があれば、それも処理する. 
            [^]]+：[ や ] 以外の文字を1つ以上（+）探す．「^」は意外という意味(ex.[^a] は「文字 a 以外」を探す)
            ?：「この部分はあってもなくてもいい」という意味→「|」 に続く内容がある場合は処理し、ない場合は無視する
    '''
    category_pattern = re.compile(r'\[\[Category:(?P<categoryName>[^|\]]+)(?:\|[^]]+)?\]\]')
    '''
      findall() メソッドで、全マッチの「category」グループを抽出する
      findall()：文字列全体を検索し、一致するすべての部分文字列をリストとして返す
    '''
    category_names = category_pattern.findall(text)
    return category_names

filename = 'jawiki-country.json'
target_title = 'イギリス'

text = read_wikipedia_article(filename, target_title)
if not text:
    print(f"記事 '{target_title}' が見つかりませんでした。")
else:
    # カテゴリ名を抽出
    category_names = extract_category_names(text)
    if category_names:
        for name in category_names:
            print(name)
    else:
        print("カテゴリ宣言は見つかりませんでした。")
