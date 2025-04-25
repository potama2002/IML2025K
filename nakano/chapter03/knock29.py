import requests
from knock20 import find_key_in_dictlist
from knock25 import extract_basic_info
from knock27 import remove_internal_links

def get_flag_image_url(filename: str) -> str:
    """
    MediaWiki APIを使って指定された画像ファイルのURLを取得する関数
    """
    endpoint = 'https://commons.wikimedia.org/w/api.php'
    params = {
        'action': 'query',
        'titles': f'File:{filename}',
        'prop': 'imageinfo',
        'format': 'json',
        'iiprop': 'url'
    }

    response = requests.get(endpoint, params=params).json()
    #print(type(response))  # dictionary
    #print(response)  # dictionary, json形式のレスポンスを見てみる
    pages = response['query']['pages']
    for page in pages.values():
        if 'imageinfo' in page:
            return page['imageinfo'][0]['url']
    return ''

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        basic_info = extract_basic_info(article)
        cleaned_info = {k: remove_internal_links(v) for k, v in basic_info.items()}

        flag_filename = cleaned_info.get('国旗画像')
        if flag_filename:
            flag_url = get_flag_image_url(flag_filename)
            print(f"記事 {idx} の国旗画像URL: {flag_url}")
        else:
            print(f"記事 {idx} に国旗画像フィールドがありません。")
