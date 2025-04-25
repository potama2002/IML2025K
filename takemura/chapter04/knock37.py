import gzip
import json
import re
import MeCab
import unidic_lite
from collections import Counter

def clean_text(text):
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref.*?/>', '', text)
    text = re.sub(r'\[http[^\s]*\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r"''+", '', text)
    text = re.sub(r'[|=<>（）{}・./\-]', '', text)
    return text

# ✅ 名詞のみ抽出するように変更！
def parse_text(text):
    tagger = MeCab.Tagger("-d {}".format(unidic_lite.DICDIR))
    tagger.parse('')
    node = tagger.parseToNode(text)
    words = []
    while node:
        surface = node.surface
        feature = node.feature.split(',')
        if surface and feature[0] == '名詞':
            words.append(surface)
        node = node.next
    return words

def extract_texts_from_n_articles(filepath, n=10):
    texts = []
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            print(f"{i} 行目読み込み中...")
            obj = json.loads(line)
            clean = clean_text(obj['text'])
            texts.append(clean)
    return '\n'.join(texts)

if __name__ == "__main__":
    all_text = extract_texts_from_n_articles('jawiki-country.json.gz', n=10)
    words = parse_text(all_text)

    print(f"\n抽出した名詞数：{len(words)}")
    print("最初の20個の名詞：", words[:20])

    freq = Counter(words)
    print("\n▶︎ 名詞 出現頻度トップ20")
    for word, count in freq.most_common(20):
        print(f"{word}\t{count}")
