import gzip
import json
import re
from collections import Counter
import MeCab
# import CaboCha

def remove_markup(text: str) -> str:
    """
    MediaWiki マークアップ（強調、内部リンク、HTMLタグ、テンプレート、外部リンク、残ったシングルクォート）を除去する
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
    MeCabを使用して形態素解析を行い、名詞を抽出する
    """
    mecab = MeCab.Tagger()
    noun_list = []
    parsed = mecab.parse(text)
    for line in parsed.splitlines():
        if line == 'EOS':
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        surface = parts[0]
        features = parts[1].split(',')
        pos = features[0]
        # 名詞のみ抽出
        if pos == "名詞" and re.search(r'[ぁ-んァ-ン一-龥a-zA-Z]', surface):
            noun_list.append(surface)
    return noun_list

'''
def analyze_with_cabocha(text: str) -> list:
    """
    CaboChaを使用して文節単位で名詞を抽出し、記号を除外する
    """
    parser = CaboCha.Parser()
    tree = parser.parse(text)
    noun_list = []
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            surface = token.surface
            features = token.feature.split(',')
            pos = features[0]
            # 名詞のみを対象とし、記号を除外
            if pos == "名詞" and re.search(r'[ぁ-んァ-ン一-龥a-zA-Z]', surface):
                noun_list.append(surface)
    return noun_list
'''


def main():
    filepath = 'jawiki-country.json.gz'
    mecab_counter = Counter()
    cabocha_counter = Counter()

    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            text = article.get('text', '')
            # マークアップ除去
            cleaned_text = remove_markup(text)
            
            # MeCabによる名詞抽出
            mecab_nouns = analyze_with_mecab(cleaned_text)
            mecab_counter.update(mecab_nouns)
            
            """
            # CaboChaによる名詞抽出
            cabocha_nouns = analyze_with_cabocha(cleaned_text)
            cabocha_counter.update(cabocha_nouns)
            """

    # MeCabによる出現頻度上位20語
    print("MeCabによる名詞の出現頻度 - 上位20語")
    for word, freq in mecab_counter.most_common(20):
        print(f"{word}: {freq}")

    """
    # CaboChaによる出現頻度上位20語
    print("\nCaboChaによる名詞の出現頻度 - 上位20語")
    for word, freq in cabocha_counter.most_common(20):
        print(f"{word}: {freq}")
    """

if __name__ == '__main__':
    main()

'''
＜実行結果＞
MeCabによる名詞の出現頻度 - 上位20語
年: 27533
月: 11934
日: 9415
人: 9354
国: 8104
語: 5517
的: 5086
こと: 4592
世界: 4252
日本: 3617
大統領: 3594
ため: 3441
州: 3291
政府: 3225
島: 3165
者: 3142
thumb: 3021
経済: 2874
共和: 2826
人口: 2786
'''