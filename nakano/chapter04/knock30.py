#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CaboCha

def extract_verbs(text: str):
    """
    CaboChaを使ってテキストを解析し、動詞リストを返す。
    """
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    verbs = []

    # トークンごとに走査
    for i in range(tree.token_size()):
        token = tree.token(i)
        surface = token.surface
        features = token.feature.split(',')
        pos = features[0]  # 品詞

        # 動詞だけを抽出
        if pos == "動詞":
            verbs.append(surface)

    return verbs

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """

    verbs = extract_verbs(text)

    print("◆ 動詞:", verbs)




'''
def extract_info(text: str):
    """
    CaboCha を使ってテキストを解析し、
    - 動詞リスト
    - 動詞とその原型のタプルリスト
    - 「AのB」名詞句リスト
    を返す。
    """
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    verbs = []
    verb_bases = []
    noun_phrases = []

    # トークンごとに走査
    print(tree.token_size())
    for i in range(tree.token_size()):
        token = tree.token(i)
        surface = token.surface
        features = token.feature.split(',')
        pos = features[0]           # 品詞
        base = features[6] if len(features) > 6 else surface  # 原型

        # 30. 動詞
        if pos == "動詞":
            verbs.append(surface)
            # 31. 動詞の原型
            verb_bases.append((surface, base))

    # 32. 「AのB」名詞句
    #  名詞＋「の」＋名詞 になるトークンの連続を探す
    for i in range(tree.token_size() - 2):
        t1 = tree.token(i)
        t2 = tree.token(i + 1)
        t3 = tree.token(i + 2)
        f1 = t1.feature.split(',')[0]
        f3 = t3.feature.split(',')[0]

        if f1 == "名詞" and t2.surface == "の" and f3 == "名詞":
            noun_phrases.append(t1.surface + "の" + t3.surface)

    return verbs, verb_bases, noun_phrases

if __name__ == "__main__":
    #text = "太郎はこの本を二郎を見た女性に渡した。"

    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    
    verbs, verb_bases, noun_phrases = extract_info(text)

    print("◆ 動詞:", verbs)
    print("◆ 動詞と原型:", verb_bases)
    print("◆ 「AのB」名詞句:", noun_phrases)

'''