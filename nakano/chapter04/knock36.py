#!/usr/bin/env python3
# coding: utf-8

import json
from collections import Counter
import MeCab

def parse_wikipedia_corpus(file_path: str):
    mecab = MeCab.Tagger("-Ochasen")
    counter = Counter()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            text = article['text']
            node = mecab.parseToNode(text)
            while node:
                surface = node.surface.strip()
                if surface:
                    counter[surface] += 1
                node = node.next
    return counter.most_common(20)

if __name__ == "__main__":
    freq = parse_wikipedia_corpus('jawiki-country.json')
    print("頻出上位20単語:")
    for word, count in freq:
        print(f"{word}\t{count}")
