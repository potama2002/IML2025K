import MeCab

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

def extract_verbs(text):
    mecab = MeCab.Tagger()
    verbs = []
    parsed = mecab.parse(text)
    for line in parsed.splitlines():
        if line == "EOS" or line == "":
            continue
        parts = line.split("\t")
        if len(parts) > 1:
            word_info = parts[1].split(",")
            if word_info[0] == "動詞":  # Extract verbs
                verbs.append(parts[0])
    return verbs

verbs = extract_verbs(text)
print("動詞:", verbs)

'''
＜実行結果＞
動詞: ['し', '除か', 'なら', 'し', 'わから', '吹き', '遊ん', '暮し', '来']
'''