#!/usr/bin/env python3
# coding: utf-8
import CaboCha
import pydot

def visualize_dependency_tree(text: str, filename="dependency_tree.png"):
    parser = CaboCha.Parser()
    tree = parser.parse(text)

    graph = pydot.Dot(graph_type='digraph')

    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_surface = "".join([tree.token(j).surface for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size)])
        node_from = pydot.Node(f"{i}: {chunk_surface}")
        graph.add_node(node_from)
        if chunk.link != -1:
            dst_chunk = tree.chunk(chunk.link)
            dst_surface = "".join([tree.token(j).surface for j in range(dst_chunk.token_pos, dst_chunk.token_pos + dst_chunk.token_size)])
            node_to = pydot.Node(f"{chunk.link}: {dst_surface}")
            graph.add_node(node_to)
            graph.add_edge(pydot.Edge(node_from, node_to))

    graph.write_png(filename)

if __name__ == "__main__":
    text = """
    メロスは激怒した。
    必ず、かの邪智暴虐の王を除かなければならぬと決意した。
    メロスには政治がわからぬ。
    メロスは、村の牧人である。
    笛を吹き、羊と遊んで暮して来た。
    けれども邪悪に対しては、人一倍に敏感であった。
    """
    visualize_dependency_tree(text)
