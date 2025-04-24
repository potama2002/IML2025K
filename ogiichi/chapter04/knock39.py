import gzip
import json
import re
from collections import Counter
import MeCab
import CaboCha
import matplotlib.pyplot as plt
from matplotlib import rcParams

def remove_markup(text: str) -> str:
    """
    MediaWiki マークアップ（強調、内部リンク、HTMLタグ、テンプレート、外部リンク、残ったシングルクォート）を除去する
    """
    text = re.sub(r"('{2,5})(.+?)\1", r'\2', text)  # 強調マークアップ除去
    text = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', text)  # 内部リンク除去
    text = re.sub(r'<.*?>', '', text)  # HTMLタグ除去
    text = re.sub(r'\{\{.*?\}\}', '', text)  # テンプレート除去
    text = re.sub(r'\[.*?\]', '', text)  # 外部リンク除去
    text = re.sub(r'\'+', '', text)  # シングルクォート除去
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
        if pos == "名詞" and re.search(r'[ぁ-んァ-ン一-龥a-zA-Z]', surface):
            noun_list.append(surface)
    return noun_list

def analyze_with_cabocha(text: str) -> list:
    """
    CaboChaを使用して文節単位で名詞を抽出する
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
            if pos == "名詞" and re.search(r'[ぁ-んァ-ン一-龥a-zA-Z]', surface):
                noun_list.append(surface)
    return noun_list

def main():
    filepath = "jawiki-country.json.gz"
    mecab_counter = Counter()
    cabocha_counter = Counter()

    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            text = article.get("text", "")
            cleaned_text = remove_markup(text)
            # MeCabによる名詞抽出
            mecab_nouns = analyze_with_mecab(cleaned_text)
            mecab_counter.update(mecab_nouns)
            # CaboChaによる名詞抽出
            cabocha_nouns = analyze_with_cabocha(cleaned_text)
            cabocha_counter.update(cabocha_nouns)

    mecab_freq_list = sorted(mecab_counter.values(), reverse=True)
    cabocha_freq_list = sorted(cabocha_counter.values(), reverse=True)
    ranks_mecab = range(1, len(mecab_freq_list) + 1)
    ranks_cabocha = range(1, len(cabocha_freq_list) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(ranks_mecab, mecab_freq_list, marker="o", label="MeCab", linestyle="None")
    plt.plot(ranks_cabocha, cabocha_freq_list, marker="x", label="CaboCha", linestyle="None")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Rank of Word Frequency (log scale)")
    plt.ylabel("Word Frequency (log scale)")
    plt.title("Word Frequency Distribution (Log-Log Graph)")
    plt.legend()
    plt.grid(which="both", linestyle="--", alpha=0.6)
    plt.show()

if __name__ == "__main__":
    main()
