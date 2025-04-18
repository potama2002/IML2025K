import json
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
基礎情報以降を抽出
.：任意の1文字．ただし改行だけ除外されている
   → re.DOTALL()を使用することで全ての任意の1文字になる
''' 
pattern = r'基礎情報(.*?<references/>)'
result = re.findall(pattern, text, re.DOTALL)
# 次のフィールド抽出の時に(改行を)使用するため
result[0] += "\n"

'''
各フィールドを抽出（改行＋パイプ(|)に続く "フィールド名 = 値" の形式）
(?<=...)：「肯定の後読み」と呼ばれる．「ある特定のパターン（ここでは改行＋縦棒）が直前にある場合だけ次をマッチさせる」という意味
          →(?<=\n\|):「\n| の直後にあるもの」を探す
(.*?)：最短一致で何でも好きな文字を探す
  .：任意の文字
  *：0回以上繰り返す
 *= *：「=」の前後に0個以上の空白があるものを探す

'''
pattern_fields = r'(?<=\n\|)(.*?) *= *(.*?)(?=\n)'
result2 = re.findall(pattern_fields, result[0], re.DOTALL)

# 辞書オブジェクトへ格納
inf_dic = {}
'''
フィールド名がkey，値がvalue
ex.
  略名  =イギリス
  key：略名
  value：イギリス
'''
for key, value in result2:
    inf_dic[key] = value

# 辞書の内容を改行して出力
for key, value in inf_dic.items():
    print(f"{key} : {value}")
