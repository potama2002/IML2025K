import json
import re
import pandas as pd

filename = "jawiki-country.json"
j_data = pd.read_json(filename, lines =True)
df = j_data
uk_df = df[df["title"]=="イギリス"]
uk_df = uk_df["text"].values
print(uk_df)

# 20

with open('jawiki-country.json', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        if data.get('title') == 'イギリス':
                data_UK = data
                break

print(data_UK)
print()
print("--- 21 ---")
print()

# 21
category_pattern = re.compile(r'\[\[(Category|カテゴリ):(.+?)(\|.*)?\]\]')

# テキストを行ごとに分割
uk_text_lines = data_UK.get('text', '').split('\n')
uk_text_string  = ''.join(uk_text_lines)
# data_UK dict
# uk_text_lines list

# カテゴリを含む行を抽出
for text_line in uk_text_lines:
    if category_pattern.search(text_line):
        print(text_line)


print()
print("--- 22 ---")
print()

for text_line in uk_text_lines:
    m = re.findall(r'\[\[Category:([^\]\|]*)', text_line) # a capture group that matches any characters except ] or |
    if m:
        print(m)

print()
print("--- 23 ---")
print()

for text_line in uk_text_lines:
    m = re.match(r'(=+\S[^=]*\S=+)', text_line)
    if m:
         section = m.group(1)
         word = re.match(r'=+\s*([^=]+?)\s*=+', section)
        #  print()
         print(f"セクション名:{word.group(1)}, レベル: {int(section.count('=')/2 -1)}")
print()
print("--- 24 ---")
print()

for text_line in uk_text_lines:
     m = re.findall(r'\[\[ファイル:([^\]\|]*)', text_line)
     if m:
          print(m)

print()
print("--- 25 ---")
print()

m = re.search(r'基礎情報(.*)', uk_text_string)
# print(m.group(1))

data = m.group(1)

# print("="*30)
# for k, v in data_info.items():
#     print("")
#     print(k, ':', v)

dic={}
for text in uk_df[0].split("\n"):
    if re.search("\|(.+?)\s=\s*(.+)", text):
        match_txt = re.search("\|(.+?)\s*=\s*(.+)", text)
        dic[match_txt[1]] = match_txt[2]
# print(dic)

print()
print("--- 26 ---")
print()

for text in uk_df[0].split("\n"):
    if re.search("\|(.+?)\s=\s*(.+)", text):
        match_txt = re.search("\|(.+?)\s=\s*(.+)", text)
        dic[match_txt[1]] = match_txt[2]
    match_sub = re.sub("\'{2,}(.+?)\'{2,}", "\\1", text)
    # print(match_sub)

print()
print("--- 27 ---")
print()

for text in uk_df[0].split("\n"):
    if re.search("\|(.+?)\s=\s*(.+)", text):
        match_txt = re.search("\|(.+?)\s=\s*(.+)", text)
        dic[match_txt[1]] = match_txt[2]
    match_sub = re.sub("\'{2,}(.+?)\'{2,}", r"\1", text)
    match_sub = re.sub("\[\[(.+?)\]\]", r"\1", match_sub)
    # print(match_sub)

print()
print("--- 28 ---")
print()

for text in uk_df[0].split("\n"):
    if re.search("\|(.+?)\s=\s*(.+)", text):
        match_txt = re.search("\|(.+?)\s=\s*(.+)", text)
        dic[match_txt[1]] = match_txt[2]
    match_sub = re.sub("\'{2,}(.+?)\'{2,}", r"\1", text) # 強調マークアップ
    match_sub = re.sub("\[\[(.+?)\]\]", r"\1", match_sub) # 内部リンク
    match_sub = re.sub("\[(.+?)\]", r"\1", match_sub) # 外部リンク
    match_sub = re.sub("\*{1,}(.+?)", r"\1", match_sub) # *箇条書き
    match_sub = re.sub("{{2,}(.+?)\}{2,}", r"\1", match_sub) # {{}}で囲まれたもの
    match_sub = re.sub("\:(.+?)", r"\1", match_sub) # : 
    print(match_sub)

print()
print("--- 29 ---")
print()

import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "prop": "imageinfo",
    "titles": f"File:{dic['国旗画像']}",
    "iiprop":"url"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
PAGES = DATA["query"]["pages"]

for k, v in PAGES.items():
    print(v["imageinfo"][0]["url"])