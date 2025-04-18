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
            uk_text = article['text']
            break

# 25: テンプレートの抽出と辞書化
template_match = re.search(r'{{基礎情報 国(.*?)\n}}', uk_text, re.DOTALL)

if template_match:
    template_text = template_match.group(1)
    info_dict = {}

    for line in template_text.split('\n|')[1:]:
        key_value_match = re.match(r'([^=]+?)\s*=\s*(.*)', line)
        if key_value_match:
            key = key_value_match.group(1).strip()
            value = key_value_match.group(2).strip()
            info_dict[key] = value

    # 26: 強調マークアップの除去
    
# 新しい辞書を作成（加工後のデータをここに入れていく）
cleaned_dict = {}

# info_dict（25番で作成したテンプレート辞書）から1項目ずつ取り出して処理
for key, value in info_dict.items():
    # re.sub(pattern, repl, string) は「文字列中のパターンを repl に置き換える」
    # 今回は、連続するシングルクォート（'）2〜5個にマッチして、それを ''（空文字）に置換＝削除
    # → MediaWikiの強調マークアップ（''斜体''、'''太字'''、'''''太字+斜体''''') を除去
    cleaned_value = re.sub(r"'{2,5}", '', value)

    # 加工済みの値を新しい辞書に追加
    cleaned_dict[key] = cleaned_value

for key, value in cleaned_dict.items():
    print('{}: {}'.format(key, value))

