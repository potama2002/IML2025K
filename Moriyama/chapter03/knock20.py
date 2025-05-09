import gzip
import json

# ファイルパス（ダウンロードしてローカルに保存したパスを指定）
file_path = '/Users/takeru/Desktop/src‘ę3¸Ķbuk/Moriyama/chapter03/jawiki-country.json.gz'

# イギリスの記事を探す
with gzip.open(file_path, 'rt', encoding='utf-8') as f: #ファイルのオープン・クローズを自動で行ってくれる構文。
    for line in f:#ファイルオブジェクト f から 1行ずつ ループで取り出します。
        article = json.loads(line) #json.loads() は、JSON形式の文字列をPythonの辞書に変換します。
        if article['title'] == 'イギリス': 
            print(article['text'])  # 記事の本文を表示
            break

