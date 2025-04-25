import gzip
import json
import re
import MeCab
import math
from collections import Counter, defaultdict

# マークアップ除去の関数（前回と同じ）
def remove_markup(text):
    # 見出しタグを削除
    text = re.sub(r'={2,}(.+?)={2,}', r'\1', text)
    
    # 特定のマークアップパターン
    text = re.sub(r"'''", '', text)  # 太字
    text = re.sub(r"''", '', text)   # 斜体
    text = re.sub(r'\*\*', '', text)  # リスト記号
    
    # ファイル・画像タグを削除
    text = re.sub(r'\[\[(ファイル|画像|File|Image):.*?\]\]', '', text)
    
    # テンプレート（入れ子構造対応）
    depth = 3
    template_pattern = r'{{[^{}]*(?:{{[^{}]*}}[^{}]*)*}}'
    for _ in range(depth):
        text = re.sub(template_pattern, '', text)
    
    # カテゴリタグを削除
    text = re.sub(r'\[\[Category:.*?\]\]', '', text)
    
    # HTMLタグを削除
    text = re.sub(r'<[^>]+>', '', text)
    
    # 内部リンク
    text = re.sub(r'\[\[([^|]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    
    # 外部リンク
    text = re.sub(r'\[https?://[^ ]+ (.*?)\]', r'\1', text)
    text = re.sub(r'\[https?://[^ ]+\]', '', text)
    
    # テーブル記法
    text = re.sub(r'\{\|[\s\S]*?\|\}', '', text)
    
    # 各種記号を削除
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'=+', '', text)
    text = re.sub(r'thumb', '', text)
    text = re.sub(r'px', '', text)
    text = re.sub(r'right', '', text)
    text = re.sub(r'align', '', text)
    
    # 連続する空白を1つに
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# ファイルからデータを読み込む
def load_wikipedia_corpus(filename):
    corpus = []
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            title = data.get('title', '')
            text = data.get('text', '')
            
            # マークアップを除去
            clean_text = remove_markup(text)
            
            corpus.append({
                'title': title,
                'text': clean_text
            })
    return corpus

# 各記事の名詞を抽出
def extract_nouns(corpus):
    tagger = MeCab.Tagger()
    
    # 除外する単語パターン
    exclude_pattern = re.compile(r'^[0-9a-zA-Z.,_:;=\-\*\"\(\)\[\]\{\}]+$')
    
    documents = []
    japan_doc_index = -1
    
    for i, article in enumerate(corpus):
        title = article['title']
        text = article['text']
        
        # 日本の記事を探す
        if title == '日本' or '日本国' in title:
            japan_doc_index = i
        
        # 名詞を抽出
        nouns = []
        node = tagger.parseToNode(text)
        
        while node:
            if node.surface and node.surface.strip():
                features = node.feature.split(',')
                pos = features[0]
                
                if (pos == '名詞' and 
                    len(node.surface) > 1 and
                    not exclude_pattern.match(node.surface)):
                    
                    nouns.append(node.surface)
            
            node = node.next
        
        documents.append(nouns)
    
    return documents, japan_doc_index

# TF-IDFを計算
def calculate_tfidf(documents, target_doc_index):
    if target_doc_index < 0 or target_doc_index >= len(documents):
        raise ValueError("対象の文書が見つかりませんでした")
    
    # 文書の総数
    N = len(documents)
    
    # 対象文書の単語頻度（TF）
    target_doc = documents[target_doc_index]
    tf = Counter(target_doc)
    
    # 各単語が出現する文書数を計算（DF）
    df = defaultdict(int)
    for doc in documents:
        # 各文書で一度でも出現した単語を記録
        words_in_doc = set(doc)
        for word in words_in_doc:
            df[word] += 1
    
    # TF-IDFの計算
    tfidf = {}
    for word, freq in tf.items():
        # TF = 単語の出現回数 / 文書の総単語数
        tf_value = freq / len(target_doc)
        
        # IDF = log(総文書数 / 単語が出現する文書数)
        idf_value = math.log(N / df[word]) if df[word] > 0 else 0
        
        # TF-IDF = TF * IDF
        tfidf[word] = (tf_value, idf_value, tf_value * idf_value)
    
    return tfidf

# メイン処理
filename = 'jawiki-country.json.gz'
try:
    # コーパスを読み込む
    corpus = load_wikipedia_corpus(filename)
    print(f"読み込んだ記事数: {len(corpus)}")
    
    # 各記事から名詞を抽出
    documents, japan_doc_index = extract_nouns(corpus)
    
    if japan_doc_index >= 0:
        print(f"日本に関する記事のインデックス: {japan_doc_index}")
        
        # TF-IDFを計算
        tfidf_scores = calculate_tfidf(documents, japan_doc_index)
        
        # TF-IDFスコアで降順ソート
        sorted_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1][2], reverse=True)
        
        # 上位20語を表示
        print("\n日本に関する記事のTF-IDFスコア上位20語:")
        print("単語\tTF\tIDF\tTF-IDF")
        print("-" * 40)
        for word, (tf, idf, tfidf) in sorted_tfidf[:20]:
            print(f"{word}\t{tf:.6f}\t{idf:.6f}\t{tfidf:.6f}")
    else:
        print("日本に関する記事が見つかりませんでした。")
        
except FileNotFoundError:
    print(f"ファイル {filename} が見つかりません。")
    print("ファイルパスを確認してください。")