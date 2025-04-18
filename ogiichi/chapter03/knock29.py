import json
import re
import urllib.request
import urllib.parse

#jsonファイル読取関数
def read_wikipedia_article(filename, target_title):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            if article.get('title') == target_title:
                return article.get('text')
    return None

filename = 'jawiki-country.json'
target_title = 'イギリス'

text = read_wikipedia_article(filename, target_title)

# 基礎情報テンプレート部分を抽出
basic_pattern = r'基礎情報(.*?<references/>)'
m = re.search(basic_pattern, text, re.DOTALL)
if m:
    basic_text = m.group(1)
    # 末尾が抜けないように改行を追加
    basic_text += "\n"
else:
    basic_text = ''

# 各フィールドの抽出
fields = re.findall(r'(?<=\n\|)(.*?) *= *(.*?)(?=\n)', basic_text, re.DOTALL)

'''
「国旗画像」フィールドの値を取得（見つからなければ None）

fields:：ここには記事のデータがキーと値のペア（例えば「タイトル」と「内容」）として格納されている
動き：キーが「国旗画像」の場合、その値を取り出して flag_image に保存する
     もし「国旗画像」が見つからない場合、flag_image は None のまま
'''
flag_image = None
for key, value in fields:
    if key.strip() == "国旗画像":
        flag_image = value.strip()
        break

if flag_image is None:
    print("国旗画像フィールドが見つかりません")
else:
    # テンプレート部分（{{...}}）の除去
    flag_image = re.sub(r'\{\{.*?\}\}', '', flag_image).strip()
    
    ''' 
    MediaWiki API に問い合わせる URL を作成

    取得した国旗画像の名前を使い、MediaWiki API にアクセスするためのURLを作成する。
    urllib.parse.quote(flag_image): 画像名に特殊文字が含まれている場合，それを正しく扱えるように変換する
    '''
    url = ('https://www.mediawiki.org/w/api.php?action=query&titles=File:' +
           urllib.parse.quote(flag_image) +
           '&format=json&prop=imageinfo&iiprop=url')
    
    '''
    API にアクセスして JSON データを取得
    作成したURLを使ってMediaWiki APIにアクセスする
    APIの結果はJSON形式（テキストデータ）で返されるから，それをPythonの辞書形式に変換する
    → json.loads を使用
    '''
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as connection:
        response = json.loads(connection.read().decode())
     
    '''
    対象画像の URL を抽出（ページIDは -1 となるケースが多い）
    APIで取得したデータから画像のURLを抜き出す
    ['query']['pages']['-1']['imageinfo'][0]['url'] の部分で、URLにアクセスする
    '''
    image_url = response['query']['pages']['-1']['imageinfo'][0]['url']
    
    # 改行付きで出力
    print(image_url + "\n")
