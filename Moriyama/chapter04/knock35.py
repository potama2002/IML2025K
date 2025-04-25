import spacy

# GiNZAモデルの読み込み
nlp = spacy.load("ja_ginza-5.2.0/ja_ginza/ja_ginza-5.2.0")

text = """
メロスは激怒した。
"""

# GiNZAで解析
doc = nlp(text)

# 各トークンの係り受けを出力
for token in doc:
    if token.dep_ != "punct":  # 句読点は無視
        print(f"{token.text} → {token.head.text}（関係: {token.dep_}）")

"""実行結果
 → メロス（関係: compound）
メロス → 激怒（関係: nsubj）
は → メロス（関係: case）
激怒 → 激怒（関係: ROOT）
し → 激怒（関係: aux）
た → 激怒（関係: aux）
"""