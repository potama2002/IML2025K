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

pattern = r'基礎情報(.*?<references/>)'
result = re.findall(pattern, text, re.DOTALL)
result[0] += "\n"

pattern_fields = r'(?<=\n\|)(.*?) *= *(.*?)(?=\n)'
result2 = re.findall(pattern_fields, result[0], re.DOTALL)

inf_dic = { key: value for key, value in result2 }
inf_dic2 = { key: re.sub(r"(\'{2,5})", "", value) for key, value in result2 }

# 各フィールドの値から不要なマークアップを除去して新しい辞書 inf_dic3 を作成
inf_dic3 = {}
for key, text in inf_dic2.items():
    # [[記事名|表示文字]] または [[記事名#節名|表示文字]] → 表示文字
    pattern1 = r"\[\[.*?\|(.*?)\]\]"
    text = re.sub(pattern1, r"\1", text)
    
    # [[記事名]] または [[記事名#節名]] → 記事名
    pattern2 = r"\[\[(.*?)(?:#.*?)?\]\]"
    text = re.sub(pattern2, r"\1", text)

    # ファイルマークアップ: [[ファイル:名前|オプション|説明文]] → 説明文
    pattern3 = r"\[\[ファイル:.*?\|.*?\|(.+?)\]\]"
    text = re.sub(pattern3, r"\1", text)

    # 外部リンク: [https://www.example.org 表示文字] → 表示文字
    pattern4 = r"\[https?:\/\/[^\s]+\s(.+?)\]"
    text = re.sub(pattern4, r"\1", text)

    # 外部リンク（リンクのみ）: [https://www.example.org] → 空文字（削除）
    pattern5 = r"\[https?:\/\/[^\s]+\]"
    text = re.sub(pattern5, '', text)

    # URL: https://www.example.org → 空文字（削除）
    pattern6 = r"https?:\/\/[^\s]+"
    text = re.sub(pattern6, '', text)

    # リダイレクトマークアップ: #REDIRECT [[記事名]] → 記事名
    pattern7 = r"#REDIRECT\[\[(.*?)\]\]"
    text = re.sub(pattern7, r"\1", text)

    # 余分なHTMLタグや構文を削除（例: <br>, <ref> など）
    pattern8 = r"<.*?>"
    text = re.sub(pattern8, '', text)

    # 整形結果を新しい辞書に格納
    inf_dic3[key] = text

# 各フィールドとその値を、改行して出力
for key, value in inf_dic3.items():
    print(f"{key} : {value}")
