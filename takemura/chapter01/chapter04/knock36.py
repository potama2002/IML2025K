import gzip
import json
import re
import MeCab
import unidic_lite
from collections import Counter

# ✅ 強化版クレンジング（refタグ + 記号 . / - を除去）
def clean_text(text):
    # {{テンプレート}}を除去
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    # [[内部リンク]] → 表示名だけ残す
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    # <ref>タグ除去（複数行にも対応）
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref.*?/>', '', text)
    # 外部リンクの表示名だけ残す → [http... 表示] → 表示
    text = re.sub(r'\[http[^\s]*\s+([^\]]+)\]', r'\1', text)
    # 太字・斜体記法（'''''）除去
    text = re.sub(r"''+", '', text)
    # その他ノイズ記号除去（.|/=<>など）
    text = re.sub(r'[|=<>（）{}・./\-]', '', text)
    return text

def parse_text(text):
    tagger = MeCab.Tagger("-d {}".format(unidic_lite.DICDIR))
    tagger.parse('')  # 初期化バグ回避
    node = tagger.parseToNode(text)
    words = []
    while node:
        surface = node.surface
        feature = node.feature.split(',')
        if surface and feature[0] != 'BOS/EOS':
            words.append(surface)
        node = node.next
    return words

def extract_texts_from_n_articles(filepath, n=10):
    texts = []
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            print(f"{i} 行目読み込み中...")
            obj = json.loads(line)
            clean = clean_text(obj['text'])
            texts.append(clean)
    return '\n'.join(texts)

if __name__ == "__main__":
    all_text = extract_texts_from_n_articles('jawiki-country.json.gz', n=10)
    words = parse_text(all_text)

    # ✅ デバッグ出力
    print(f"\n抽出した単語数：{len(words)}")
    print("最初の20単語：", words[:20])

    # ✅ 頻度カウントと出力
    freq = Counter(words)
    print("\n▶︎ 出現頻度トップ20")
    for word, count in freq.most_common(20):
        print(f"{word}\t{count}")
