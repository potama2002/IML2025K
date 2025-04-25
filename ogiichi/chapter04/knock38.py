import gzip
import json
import re
from collections import Counter, defaultdict
import MeCab
import CaboCha
import math

def remove_markup(text: str) -> str:
    """
    マークアップを除去する
    """
    text = re.sub(r"('{2,5})(.+?)\1", r'\2', text)
    text = re.sub(r'\[\[.*?\|?(.+?)\]\]', r'\1', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\{\{.*?\}\}', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\'+', '', text)
    return text.strip()

def analyze_with_mecab(text: str):
    """
    MeCabによる形態素解析
    """
    mecab = MeCab.Tagger()
    term_freq = Counter()
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
            term_freq[surface] += 1
    return term_freq

def analyze_with_cabocha(text: str):
    """
    CaboChaによる構文解析
    """
    parser = CaboCha.Parser()
    tree = parser.parse(text)
    dependencies = []
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        tokens = []
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            surface = token.surface
            features = token.feature.split(',')
            pos = features[0]
            if pos == "名詞":
                tokens.append(surface)
        # 文節内の名詞をリストとして記録
        if tokens:
            dependencies.append(tokens)
    return dependencies

def calculate_tf_idf(file_path: str, query: str):
    doc_freq = defaultdict(int)
    term_freqs = []
    num_documents = 0

    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            title = article.get('title', '')
            text = article.get('text', '')

            if query not in title:
                continue

            cleaned_text = remove_markup(text)

            # MeCabで形態素解析
            term_freq = analyze_with_mecab(cleaned_text)
            term_freqs.append(term_freq)

            # CaboChaで構文解析（必要に応じて使用）
            dependencies = analyze_with_cabocha(cleaned_text)

            for word in term_freq.keys():
                doc_freq[word] += 1

            num_documents += 1

    if num_documents == 0:
        print("対象記事が見つかりませんでした。")
        return

    # IDF計算
    idf = {word: math.log((num_documents + 1) / (df + 1)) + 1 for word, df in doc_freq.items()}

    # TF・IDF計算
    tf_idf_scores = Counter()
    for term_freq in term_freqs:
        for word, tf in term_freq.items():
            tf_idf = tf * idf[word]
            tf_idf_scores[word] += tf_idf

    print("名詞のTF・IDFスコア上位20語")
    print("単語\tTF\tIDF\tTF・IDF")
    for word, score in tf_idf_scores.most_common(20):
        tf_total = sum(tf[word] for tf in term_freqs if word in tf)
        idf_val = idf[word]
        print(f"{word}\t{tf_total:.2f}\t{idf_val:.2f}\t{score:.2f}")

if __name__ == "__main__":
    calculate_tf_idf("jawiki-country.json.gz", "日本")

'''
＜実行結果＞
名詞のTF・IDFスコア上位20語
単語	TF	IDF	TF・IDF
日本	825.00	1.00	825.00
年	656.00	1.00	656.00
国	263.00	1.00	263.00
的	220.00	1.00	220.00
日	196.00	1.00	196.00
県	178.00	1.00	178.00
人	169.00	1.00	169.00
世界	165.00	1.00	165.00
こと	162.00	1.00	162.00
月	160.00	1.00	160.00
関係	126.00	1.00	126.00
経済	120.00	1.00	120.00
中国	114.00	1.00	114.00
地方	96.00	1.00	96.00
地域	96.00	1.00	96.00
ため	94.00	1.00	94.00
憲法	91.00	1.00	91.00
政府	90.00	1.00	90.00
化	86.00	1.00	86.00
時代	84.00	1.00	84.00
'''