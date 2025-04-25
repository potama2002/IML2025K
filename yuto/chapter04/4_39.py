import gzip
import json
import re
import MeCab
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import matplotlib as mpl

# 日本語フォントの設定
# macOSの場合
plt.rcParams['font.family'] = 'Hiragino Sans GB'
# Windowsの場合は以下をコメント解除
# plt.rcParams['font.family'] = 'MS Gothic'
# Linuxの場合は以下をコメント解除
# plt.rcParams['font.family'] = 'IPAGothic'

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

# コーパス内の単語出現頻度を計算
def count_word_frequency(corpus):
    tagger = MeCab.Tagger()
    word_counter = Counter()
    
    # 除外する品詞
    exclude_pos = ['助詞', '助動詞', '記号', '接頭詞', '接続詞', '連体詞']
    
    # 除外する単語パターン
    exclude_pattern = re.compile(r'^[0-9a-zA-Z.,_:;=\-\*\"\(\)\[\]\{\}]+$')
    
    for article in corpus:
        text = article['text']
        node = tagger.parseToNode(text)
        
        while node:
            if node.surface and node.surface.strip():
                features = node.feature.split(',')
                pos = features[0]  # 品詞
                
                # 除外する品詞や単語パターンでないもののみカウント
                if (pos not in exclude_pos and 
                    len(node.surface) > 1 and  # 1文字の単語を除外
                    not exclude_pattern.match(node.surface)):
                    
                    word_counter[node.surface] += 1
            
            node = node.next
    
    return word_counter

# Zipfの法則のグラフをプロット
def plot_zipf_law(word_counter):
    # 出現頻度でソート
    word_counts = word_counter.most_common()
    
    # 順位と頻度を抽出
    ranks = list(range(1, len(word_counts) + 1))
    frequencies = [count for word, count in word_counts]
    
    # 両対数グラフをプロット
    plt.figure(figsize=(12, 8))
    plt.loglog(ranks, frequencies, marker='.', linestyle='none', alpha=0.5)
    
    # 理論的なZipfの法則のラインを追加（比較用）
    max_freq = frequencies[0]
    zipf_law = [max_freq / r for r in ranks]
    plt.loglog(ranks, zipf_law, 'r-', alpha=0.8, label='理論値 (1/rank)')
    
    # グラフにラベルを設定
    plt.xlabel('単語の出現頻度順位', fontsize=14)
    plt.ylabel('出現頻度', fontsize=14)
    plt.title('Zipfの法則 - 単語の出現頻度と順位（両対数グラフ）', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # 高頻度の単語をプロット上に表示（上位10語）
    '''for i in range(min(10, len(word_counts))):
        word, freq = word_counts[i]
        plt.annotate(word, 
                     xy=(i+1, freq),
                     xytext=(5, 5),
                     textcoords='offset points',
                     fontsize=12)'''
    
    plt.tight_layout()
    
    # グラフを保存
    plt.savefig('zipf_law_plot.png', dpi=300)
    
    # グラフを表示
    plt.show()

# メイン処理
filename = 'jawiki-country.json.gz'
try:
    # コーパスを読み込む
    corpus = load_wikipedia_corpus(filename)
    print(f"読み込んだ記事数: {len(corpus)}")
    
    # 単語の出現頻度を計算
    word_counter = count_word_frequency(corpus)
    print(f"異なり語数: {len(word_counter)}")
    
    # Zipfの法則のグラフをプロット
    plot_zipf_law(word_counter)
    
except FileNotFoundError:
    print(f"ファイル {filename} が見つかりません。")
    print("ファイルパスを確認してください。")