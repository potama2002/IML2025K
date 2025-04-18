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

pattern = r'基礎情報(.*?<references/>)'
result = re.findall(pattern, text, re.DOTALL)
result[0] += "\n" 

pattern_fields = r'(?<=\n\|)(.*?) *= *(.*?)(?=\n)'
result2 = re.findall(pattern_fields, result[0], re.DOTALL)

"""
ここだけ追加
key：変更なし
value：re.sub(r"(\'{2,5})", "", value) を使って，値の中から ''' のようなアポストロフィを削除する
    \': アポストロフィ（シングルクォート）を探す
    {2,5}: アポストロフィが2個以上5個以下連続している部分にマッチする
    → アポストロフィが '' や ''' のように並んでいる箇所を探す
re.sub：正規表現を使った「置換」を行う関数
        value の中で、'' や ''' を空文字（""）に置き換える → 強調マークアップをなくす
"""
inf_dic2 = { key: re.sub(r"(\'{2,5})", "", value) for key, value in result2 }

for key, value in inf_dic2.items():
    print(f"{key} : {value}")
