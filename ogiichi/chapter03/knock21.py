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

#カテゴリ宣言行の抽出を行う関数
def extract_category_lines(text):
    '''記事本文からカテゴリ宣言行 ([[Category:...]] 形式の行) を抜き出す'''
    '''
      非貪欲マッチでカテゴリ宣言を正確にマッチさせるパターン
      [Category]:で一致するものを探す
      \：エスケープ(ex.\[であれば「[」を文字として認識する)
      .：任意の一文字
      *：0回以上の繰り返し
      ?：非貪欲マッチ
        ex.
            s = 'axb-axxxxxxb'
            <貪欲マッチ>
            print(re.findall('a.*b', s))
            # ['axb-axxxxxxb']
            <非貪欲マッチ>
            print(re.findall('a.*?b', s))
            # ['axb', 'axxxxxxb']
    '''
    category_pattern = re.compile(r'\[\[Category:.*?\]\]')
    # 改行で各行に分割し、パターンにマッチする行だけを抽出
    '''
    text.splitlines()：行で区切る
    category_pattern.search(line)：[[Category:～]] の形をした行を探し出す
    '''
    category_lines = [line for line in text.splitlines() if category_pattern.search(line)]
    return category_lines

filename = 'jawiki-country.json'
target_title = 'イギリス'

text = read_wikipedia_article(filename, target_title)
if not text:
    print(f"記事 '{target_title}' が見つかりませんでした。")
else:
    #カテゴリ宣言行を抽出
    categories = extract_category_lines(text)
    if categories:
        print("抽出されたカテゴリ宣言行:")
        for line in categories:
            print(line)
    else:
        print("カテゴリ宣言行は見つかりませんでした。")
