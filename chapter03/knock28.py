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
cleaned_dict = {}

for key, value in info_dict.items():
    cleaned_value = re.sub(r"'{2,5}", '', value)

    cleaned_dict[key] = cleaned_value


#27 内部リンクの除去
linked_dict = {}

for key, value in cleaned_dict.items():
    replaced = re.sub(r'\[\[([^|\]]+)(?:\|([^|\]]*))?\]\]',
                      lambda m: m.group(2) if m.group(2) else m.group(1),
                      value)
    linked_dict[key] = replaced


#28 MediaWikiマークアップの除去
    import re

final_dict = {}

for key, value in linked_dict.items():
    # 1. <ref>...</ref> タグを除去（非貪欲マッチ）
    value = re.sub(r'<ref.*?>.*?</ref>', '', value)

    # 2. <br> などのHTMLタグを除去（<...> にマッチ）
    value = re.sub(r'<.*?>', '', value)

    # 3. {{...}} テンプレートを除去（非ネスト前提）
    value = re.sub(r'\{\{.*?\}\}', '', value)

    # 加工後の値を格納
    final_dict[key] = value

# 表示
for key, value in final_dict.items():
    print('{}: {}'.format(key, value))

