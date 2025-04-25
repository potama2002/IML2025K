#!/usr/bin/env python3
# coding: utf-8

import json
from collections import Counter
import MeCab

def noun_frequency(file_path: str):
    mecab = MeCab.Tagger()
    counter = Counter()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            text = article['text']
            node = mecab.parseToNode(text)
            while node:
                features = node.feature.split(',')
                if features[0] == "名詞":
                    surface = node.surface.strip()
                    if surface and surface not in ("|", "[[", "]]", "=", ".", "-", "/", ":", "<", ">", "{", "}", "(", ")", "「", "」", "『", "』", "【", "】", "・", "}}","{{" ):
                        counter[surface] += 1
                node = node.next
    return counter.most_common(20)

if __name__ == "__main__":
    freq = noun_frequency('jawiki-country.json')
    print("頻出上位20名詞:")
    for word, count in freq:
        print(f"{word}\t{count}")
