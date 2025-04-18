import requests
import json

def get_flag_url():
    d = remove_markups()['国旗画像']
    
    url = 'https://www.mediawiki.org/w/api.php'
    params = {
        'action': 'query',
        'titles': f'File:{d}',
        'format': 'json',
        'prop': 'imageinfo',
        'iiprop': 'url'
    }
    
    res = requests.get(url, params=params)
    data = res.json()
    
    # ページIDは動的な数値なので「最初の値を取得」する
    page = next(iter(data['query']['pages'].values()))
    return page['imageinfo'][0]['url']

# 実行してURLを表示
print(get_flag_url())
