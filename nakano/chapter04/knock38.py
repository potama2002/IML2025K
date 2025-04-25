#!/usr/bin/env python3
# coding: utf-8

import json
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_nouns(text):
    mecab = MeCab.Tagger("-Ochasen")
    node = mecab.parseToNode(text)
    nouns = []
    while node:
        features = node.feature.split(',')
        if features[0] == '名詞':
            surface = node.surface.strip()
            if surface:
                nouns.append(surface)
        node = node.next
    return ' '.join(nouns)

def compute_tfidf(file_path: str, target_article: str):
    documents = []
    titles = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            titles.append(article['title'])
            documents.append(extract_nouns(article['text']))

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)

    if target_article in titles:
        idx = titles.index(target_article)
        tfidf_scores = X[idx].toarray()[0]
        top_n = np.argsort(tfidf_scores)[::-1][:20]
        feature_names = vectorizer.get_feature_names_out()

        results = [(feature_names[i], tfidf_scores[i]) for i in top_n]
        return results
    else:
        raise ValueError(f"{target_article}という記事が見つかりません。")

if __name__ == "__main__":
    tfidf_results = compute_tfidf('jawiki-country.json', '日本')
    print("日本の記事のTF-IDF上位20名詞:")
    for word, score in tfidf_results:
        print(f"{word}\t{score:.4f}")
