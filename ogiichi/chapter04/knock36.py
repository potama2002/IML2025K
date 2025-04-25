import gzip
import json
import re
from collections import Counter
import MeCab

def remove_markup(text: str) -> str:
    """
    MediaWikiマークアップ（強調、内部リンク、HTMLタグ、テンプレート、外部リンク、シングルクォート）を除去する
    """
    text = re.sub(r"('{2,5})(.+?)\1", r'\2', text)      # 強調マークアップ除去
    text = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', text)  # 内部リンク除去
    text = re.sub(r'<.*?>', '', text)                   # HTMLタグ除去
    text = re.sub(r'\{\{.*?\}\}', '', text)             # テンプレート除去
    text = re.sub(r'\[.*?\]', '', text)                 # 外部リンク除去
    text = re.sub(r'\'+', '', text)                     # シングルクォート除去
    return text.strip()

def analyze_with_mecab(text: str) -> list:
    """
    MeCabを使用して形態素解析を行い、単語リストを返す
    """
    mecab = MeCab.Tagger("-Owakati")  # 分かち書きモードを指定
    parsed = mecab.parse(text)
    words = parsed.split() if parsed else []
    return words

def main():
    filepath = 'jawiki-country.json.gz'  # Wikipedia記事のgzip圧縮ファイル
    counter = Counter()
    
    # gzipファイルをテキストモードでオープンする
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            text = article.get('text', '')  # 記事本文を取得
            # マークアップ除去
            cleaned_text = remove_markup(text)
            # MeCabによる形態素解析
            words = analyze_with_mecab(cleaned_text)
            counter.update(words)  # 出現頻度をカウント

    # 出現頻度が高い上位20語とその頻度を表示
    print("形態素の出現頻度上位20語:")
    for word, freq in counter.most_common(20):
        print(f"{word}: {freq}")

if __name__ == '__main__':
    main()

'''
＜実行結果＞
形態素の出現頻度上位20語:
の: 89916
、: 84455
。: 51954
は: 51266
に: 48920
|: 48019
が: 43547
を: 38088
た: 34865
で: 33371
年: 27533
と: 27314
て: 25570
し: 25098
=: 18421
）: 17910
（: 17823
.: 15693
れ: 13815
いる: 13357
'''