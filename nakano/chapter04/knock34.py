#!/usr/bin/env python3
# coding: utf-8

import CaboCha

def extract_subject_predicate(text: str, subject: str):
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    predicates = []
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_surface = "".join([tree.token(j).surface for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size)])
        if subject in chunk_surface:
            dst_chunk = tree.chunk(chunk.link)
            predicate = "".join([tree.token(k).surface for k in range(dst_chunk.token_pos, dst_chunk.token_pos + dst_chunk.token_size)])
            predicates.append(predicate)
    return predicates

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    predicates = extract_subject_predicate(text, "メロス")
    print("主語「メロス」の述語:", predicates)
