import gzip
import json
import re
import MeCab
import unidic_lite
import matplotlib.pyplot as plt
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

def extract_all_words(text):
    tagger = MeCab.Tagger("-d {}".format(unidic_lite.DICDIR))
    tagger.parse('')
    node = tagger.parseToNode(text)
    words = []
    while node:
        if node.surface:
            words.append(node.surface)
        node = node.next
    return words

if __name__ == "__main__":
    counter = Counter()
    with gzip.open("jawiki-country.json.gz", "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 100:
                break
            article = json.loads(line)
            text = clean_text(article["text"])
            words = extract_all_words(text)
            counter.update(words)

    # Zipfの法則のためにログスケールで描画
    freqs = list(counter.values())
    freqs.sort(reverse=True)
    ranks = range(1, len(freqs) + 1)

    plt.figure(figsize=(8, 6))
    plt.loglog(ranks, freqs, marker=".")
    plt.xlabel("Rank (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.title("Zipf's Law: Word Frequency Distribution")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
