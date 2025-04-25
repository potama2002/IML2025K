#!/usr/bin/env python3
# coding: utf-8

import CaboCha

def extract_noun_phrases(text: str):
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    noun_phrases = []
    for i in range(tree.token_size() - 2):
        t1 = tree.token(i)
        t2 = tree.token(i+1)
        t3 = tree.token(i+2)

        f1 = t1.feature.split(',')[0]
        f3 = t3.feature.split(',')[0]

        if f1 == "名詞" and t2.surface == "の" and f3 == "名詞":
            noun_phrases.append(t1.surface + "の" + t3.surface)
    return noun_phrases

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    noun_phrases = extract_noun_phrases(text)
    print("「AのB」名詞句:", noun_phrases)
