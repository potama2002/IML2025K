#!/usr/bin/env python3
# coding: utf-8

import CaboCha

def dependency_parse(text: str):
    parser = CaboCha.Parser()
    tree = parser.parse(text)
    
    result = []
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        if chunk.link != -1:
            from_chunk = "".join([tree.token(j).surface for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size)])
            to_chunk = "".join([tree.token(j).surface for j in range(tree.chunk(chunk.link).token_pos, tree.chunk(chunk.link).token_pos + tree.chunk(chunk.link).token_size)])
            result.append((from_chunk, to_chunk))
    return result

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    deps = dependency_parse(text)
    for from_chunk, to_chunk in deps:
        print(f"{from_chunk}\t{to_chunk}")
