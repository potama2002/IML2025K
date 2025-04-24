import MeCab

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

def extract_verbs_with_base_form(text):
    mecab = MeCab.Tagger()
    verbs_with_base = []
    parsed = mecab.parse(text)
    for line in parsed.splitlines():
        if line == "EOS" or line == "":
            continue
        parts = line.split("\t")
        if len(parts) > 1:
            word_info = parts[1].split(",")
            if word_info[0] == "動詞":  # Check if the word is a verb
                surface_form = parts[0]
                base_form = word_info[6]  # Get the dictionary (base) form
                verbs_with_base.append((surface_form, base_form))
    return verbs_with_base

verbs_with_base = extract_verbs_with_base_form(text)
for verb, base_form in verbs_with_base:
    print(f"動詞: {verb}, 原型: {base_form}")

'''
＜実行結果＞
動詞: し, 原型: する
動詞: 除か, 原型: 除く
動詞: なら, 原型: なる
動詞: し, 原型: する
動詞: わから, 原型: わかる
動詞: 吹き, 原型: 吹く
動詞: 遊ん, 原型: 遊ぶ
動詞: 暮し, 原型: 暮す
動詞: 来, 原型: 来る
'''