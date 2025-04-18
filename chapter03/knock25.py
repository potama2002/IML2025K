import gzip
import json
import re


# 20: イギリスの記事を抽出
file_path = '/Users/takeru/Downloads/src‘ę3¸Ķ/Moriyama/chapter03/jawiki-country.json.gz'

uk_text = ''
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            uk_text = article['text'] # イギリス記事の本文（text）を uk_text に保存。
            break

#25 テンプレートの抽出と辞書化
        
import re  # 正規表現モジュールをインポート

# 1. 基礎情報テンプレート全体を抽出
# - re.search() は文字列から最初にマッチした1件を返す
# - r'{{基礎情報 国(.*?)\n}}' は「{{基礎情報 国」から「}}」の直前までを取得
# - re.DOTALL フラグを使うことで '.' が改行にもマッチするようになる
template_match = re.search(r'{{基礎情報 国(.*?)\n}}', uk_text, re.DOTALL)

if template_match:
    # 2. グループ1（テンプレートの中身）だけ取り出す
    template_text = template_match.group(1)

    info_dict = {}

    # 3. "\n|" で区切って各フィールド（key=value）を取り出す
    # - split('\n|') により、各行の "|key = value" を分離
    # - [1:] にすることで、最初の空要素（'{{基礎情報 国'）を除外
    for line in template_text.split('\n|')[1:]:
        # 4. "key = value" の形式にマッチする行を正規表現でパース
        # - ([^=]+?) は「= の前のキー部分」
        # - \s*=\s* は「= の前後の空白を許容」
        # - (.*) は値の部分（行末まで）
        key_value_match = re.match(r'([^=]+?)\s*=\s*(.*)', line)

        if key_value_match:
            # .group(1)：キー部分、.group(2)：値部分
            # strip() で前後の余計な空白を除去
            key = key_value_match.group(1).strip()
            value = key_value_match.group(2).strip()

            # 辞書に追加
            info_dict[key] = value
    for key, value in info_dict.items():
        print('{}: {}'.format(key, value))
