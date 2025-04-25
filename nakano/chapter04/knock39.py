#!/usr/bin/env python3
# coding: utf-8

import json
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
import numpy as np

def get_word_frequency(file_path: str):
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
    return counter

def plot_zipf(counter: Counter):
    frequencies = np.array(sorted(counter.values(), reverse=True))
    ranks = np.arange(1, len(frequencies) + 1)

    plt.figure(figsize=(10, 7))
    plt.plot(np.log(ranks), np.log(frequencies), marker='.', linestyle='none')
    plt.xlabel('log(頻度順位)', fontsize=14)
    plt.ylabel('log(単語頻度)', fontsize=14)
    plt.title('Zipfの法則 (単語の出現頻度 vs 頻度順位)', fontsize=16)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('zipf_law.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    counter = get_word_frequency('jawiki-country.json')
    plot_zipf(counter)
