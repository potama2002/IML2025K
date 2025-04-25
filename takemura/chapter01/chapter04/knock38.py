import gzip
import json
import re
import math
import MeCab
import unidic_lite
from collections import Counter, defaultdict

def clean_text(text):
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref.*?/>', '', text)
    text = re.sub(r'\[http[^\s]*\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r"''+", '', text)
    text = re.sub(r'[|=<>（）{}・./\-]', '', text)
    return text

def extract_nouns(text):
    tagger = MeCab.Tagger("-d {}".format(unidic_lite.DICDIR))
    tagger.parse('')
    node = tagger.parseToNode(text)
    nouns = []
    while node:
        surface = node.surface
        features = node.feature.split(',')
        if surface and features[0] == '名詞':
            nouns.append(surface)
        node = node.next
    return nouns

def compute_tfidf(corpus, keyword="日本"):
    tf = Counter()
    df = defaultdict(int)
    total_docs = 0
    matched_docs = 0

    for doc in corpus:
        total_docs += 1
        words = set(doc["nouns"])
        for word in words:
            df[word] += 1
        if keyword in doc["title"]:
            matched_docs += 1
            print(f"✅ マッチ: {doc['title']}")
            tf.update(doc["nouns"])

    print(f"\n日本を含むタイトルの記事数: {matched_docs}")
    print("TFの語数:", len(tf))
    print("最頻名詞:", tf.most_common(5))

    tfidf_list = []
    for word, freq in tf.items():
        idf = math.log(total_docs / (df[word] + 1))
        tfidf = freq * idf
        tfidf_list.append((word, freq, round(idf, 3), round(tfidf, 3)))

    tfidf_list.sort(key=lambda x: x[3], reverse=True)
    return tfidf_list[:20]

if __name__ == "__main__":
    corpus = []
    with gzip.open("jawiki-country.json.gz", "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 500:
                break
            article = json.loads(line)
            text = clean_text(article['text'])
            nouns = extract_nouns(text)
            corpus.append({"title": article["title"], "nouns": nouns})

    top_tfidf = compute_tfidf(corpus, keyword="日本")

    print("\n▶︎ 『日本』を含む記事における TF・IDF 上位20語")
    print("単語\tTF\tIDF\tTF-IDF")
    for word, tf, idf, tfidf in top_tfidf:
        print(f"{word}\t{tf}\t{idf}\t{tfidf}")
