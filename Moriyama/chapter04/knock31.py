import fugashi
import ipadic

# MeCabのipadic辞書を使ったTagger
tagger = fugashi.GenericTagger(ipadic.MECAB_ARGS)

# 対象テキスト
text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

# 動詞とその原型を出力
for word in tagger(text):
    if "動詞" in word.feature[0]:
        print(f"{word.surface}\t原型: {word.feature[6]}")




""" 実行結果
し      原型: する
た      原型: た
除か    原型: 除く
なけれ  原型: ない
なら    原型: なる
ぬ      原型: ぬ
し      原型: する
た      原型: た
わから  原型: わかる
ぬ      原型: ぬ
で      原型: だ
ある    原型: ある
吹き    原型: 吹く
遊ん    原型: 遊ぶ
暮し    原型: 暮す
来      原型: 来る
た      原型: た
で      原型: だ
あっ    原型: ある
た      原型: た
"""