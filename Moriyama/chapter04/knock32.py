import fugashi
import ipadic

tagger = fugashi.GenericTagger(ipadic.MECAB_ARGS)

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。。
"""

# トークン化（リスト化）しておく
words = list(tagger(text))

# 「名詞 + の + 名詞」のパターンを抽出
for i in range(len(words) - 2):
    if (words[i].feature[0] == "名詞" and
        words[i+1].surface == "の" and
        words[i+2].feature[0] == "名詞"):
        phrase = f"{words[i].surface}の{words[i+2].surface}"
        print(phrase)

"""実行結果
暴虐の王
村の牧人
"""