import gzip
import json
import re
import MeCab
from collections import Counter

# マークアップ除去の関数（完全版）
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
    text = re.sub(r'\[\[([^|]+)\|([^\]]+)\]\]', r'\2', text)  # [[リンク|表示文字]]
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # [[リンク]]
    
    # 外部リンク
    text = re.sub(r'\[https?://[^ ]+ (.*?)\]', r'\1', text)  # [URL 表示文字]
    text = re.sub(r'\[https?://[^ ]+\]', '', text)  # [URL]
    
    # テーブル記法
    text = re.sub(r'\{\|[\s\S]*?\|\}', '', text)
    
    # 各種記号を削除
    text = re.sub(r'\|', ' ', text)  # テーブル区切り
    text = re.sub(r'=+', '', text)   # 見出し記号の残り
    text = re.sub(r'thumb', '', text)  # サムネイル指定
    text = re.sub(r'px', '', text)  # ピクセル指定
    text = re.sub(r'right', '', text)  # 右寄せ指定
    text = re.sub(r'align', '', text)  # 配置指定
    
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

# 単語の出現頻度を計算
def count_word_frequency(corpus):
    tagger = MeCab.Tagger()
    word_counter = Counter()
    
    # 除外する品詞
    exclude_pos = ['助詞', '助動詞', '記号', '接頭詞', '接続詞', '連体詞', '感動詞']
    
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

# メイン処理
filename = 'jawiki-country.json.gz'
try:
    # コーパスを読み込む
    corpus = load_wikipedia_corpus(filename)
    print(f"読み込んだ記事数: {len(corpus)}")
    
    # 単語の出現頻度を計算
    word_frequencies = count_word_frequency(corpus)
    
    # 出現頻度の高い20語を表示
    print("\n出現頻度の高い20語:")
    for word, count in word_frequencies.most_common(20):
        print(f"{word}: {count}回")
        
except FileNotFoundError:
    print(f"ファイル {filename} が見つかりません。")
    print("ファイルパスを確認してください。")