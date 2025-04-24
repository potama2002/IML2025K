import MeCab

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

def extract_noun_phrases(text):
    mecab = MeCab.Tagger()
    noun_phrases = []
    parsed = mecab.parse(text)
    lines = parsed.splitlines()

    for i in range(len(lines) - 2):  # To check three consecutive lines
        if lines[i] == "EOS" or lines[i+1] == "EOS" or lines[i+2] == "EOS":
            continue

        parts1 = lines[i].split("\t")
        parts2 = lines[i+1].split("\t")
        parts3 = lines[i+2].split("\t")

        if len(parts1) > 1 and len(parts2) > 1 and len(parts3) > 1:
            word_info1 = parts1[1].split(",")
            word_info2 = parts2[1].split(",")
            word_info3 = parts3[1].split(",")

            if word_info1[0] == "名詞" and parts2[0] == "の" and word_info3[0] == "名詞":
                noun_phrase = parts1[0] + parts2[0] + parts3[0]
                noun_phrases.append(noun_phrase)

    return noun_phrases

noun_phrases = extract_noun_phrases(text)
print("名詞句 (2つの名詞を「の」で連結):", noun_phrases)

'''
＜実行結果＞
名詞句 (2つの名詞を「の」で連結): ['暴虐の王', '村の牧人']
'''