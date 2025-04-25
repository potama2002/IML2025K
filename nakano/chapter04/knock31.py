#!/usr/bin/env python3
# coding: utf-8

import CaboCha

def extract_verbs_and_bases(text: str):
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    verb_bases = []
    for i in range(tree.token_size()):
        token = tree.token(i)
        features = token.feature.split(',')
        pos = features[0]
        base = features[6] if len(features) > 6 else token.surface
        if pos == "動詞":
            verb_bases.append((token.surface, base))
    return verb_bases

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    verb_bases = extract_verbs_and_bases(text)
    print("動詞と原型:", verb_bases)
