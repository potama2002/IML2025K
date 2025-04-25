import re
import pandas as pd

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

'''
^：行の先頭に一致する→タイトルは行の先頭から始まっている必要がある
(=  )：連続するイコール記号 = を探し，記録する
{2,}：「2回以上」という意味(ex.== , === )
\s*：空白文字(ex. 「=== 文学 ===」の「=」と「文」の間の空白を認識)
*：0回以上
(.+?)：.+ は「1文字以上の任意の文字」を表して，記録する
?：非貪欲マッチ
\s*：空白文字（スペースやタブ）
\1:最初のキャプチャグループ（(={2,})）と同じ内容に一致する必要がある，という意味
   →最初と最後のイコールの数が一致している必要があります。
$:行の終わりに一致

re.MULTILINE:文字列を複数行として扱い，「行ごとに検索」を可能にする
re.VERBOSE:正規表現を読みやすくするために，改行やコメントを書けるようにする
'''
sections = re.findall(r'''^(={2,})\s*(.+?)\s*\1$''', text, re.MULTILINE+re.VERBOSE)

for section in sections:
    '''
    section：
      section[0]：(={2,})
        ex. ===, ==
      section[1]：(.+?) → セクション名
    '''
    level = len(section[0]) - 1    # '='の数-1
    print(section[1],level)
