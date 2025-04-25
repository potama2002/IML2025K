import MeCab
import CaboCha
import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import numpy as np
import os

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

# MeCabのタガーを初期化
tagger = MeCab.Tagger()

# CaboChaパーサーを初期化
parser = CaboCha.Parser()

# テキストを文ごとに分割
sentences = [s + '。' for s in text.strip().split('。') if s]

# 各文の係り受け木を格納するためのリスト
all_images = []
all_titles = []

# 各文をパースしてグラフ化
for i, sentence in enumerate(sentences):
    print(f"文{i+1}を解析: {sentence}")
    
    # CaboChaで解析
    tree = parser.parse(sentence)
    
    # デバッグ情報を表示
    print(f"  チャンク数: {tree.chunk_size()}")
    
    if tree.chunk_size() > 0:
        # この文をグラフ化
        graph = pydot.Dot(graph_type='digraph')
        nodes = []
        
        # 各チャンクを処理
        for j in range(tree.chunk_size()):
            chunk = tree.chunk(j)
            token_pos = chunk.token_pos
            token_size = chunk.token_size
            
            # チャンクの表層形を取得
            surface = ''.join([tree.token(token_pos + k).surface for k in range(token_size)])
            print(f"  チャンク{j}: {surface}, 係り先: {chunk.link}")
            
            # 空のチャンクは飛ばす
            if not surface:
                continue
                
            node = pydot.Node(surface)
            graph.add_node(node)
            nodes.append((node, chunk.link))
        
        # エッジを追加
        for j, (node, link) in enumerate(nodes):
            if link != -1 and link < len(nodes):
                graph.add_edge(pydot.Edge(node, nodes[link][0]))
        
        # 一時ファイルに保存
        temp_filename = f'temp_sentence_{i+1}.png'
        graph.write_png(temp_filename)
        
        # 画像を読み込む
        img = mpimg.imread(temp_filename)
        all_images.append(img)
        all_titles.append(f'文{i+1}: {sentence}')

# すべての画像を一つの大きな画像にまとめる
if all_images:
    num_images = len(all_images)
    
    # 適切なグリッドサイズを決定
    cols = min(3, num_images)  # 最大3列
    rows = (num_images + cols - 1) // cols  # 必要な行数
    
    # 大きな図を作成
    fig = plt.figure(figsize=(18, 6 * rows))
    gs = GridSpec(rows, cols, figure=fig)
    
    # 各サブプロットに画像を配置
    for i, (img, title) in enumerate(zip(all_images, all_titles)):
        row = i // cols
        col = i % cols
        
        ax = fig.add_subplot(gs[row, col])
        ax.imshow(img)
        ax.set_title(title)
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('all_dependency_trees.png', dpi=300)
    plt.show()
    
    # 一時ファイルを削除
    for i in range(len(all_images)):
        temp_file = f'temp_sentence_{i+1}.png'
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    print(f"すべての係り受け木を一つの画像にまとめました: all_dependency_trees.png")
else:
    print("有効な係り受け木が生成されませんでした。")

# # 各文をパースしてグラフ化
# sentences = text.strip().split('。')
# for i, sentence in enumerate(sentences):
#     if not sentence:  # 空の文は飛ばす
#         continue

#     print(f"解析文: {sentence}")

#     tree = parser.parse(sentence + '。')
#     print(f"文{i+1}のチャンク数: {tree.chunk_size()}")

#     if tree.chunk_size() > 0:
#         # この文をグラフ化
#         graph = pydot.Dot(graph_type='digraph')
#         nodes = []

#         for j in range(tree.chunk_size()):
#             chunk = tree.chunk(j)
#             token_pos = chunk.token_pos
#             token_size = chunk.token_size

#             # チャンクの表層形を取得
#             surface = ''.join([tree.token(token_pos + k).surface for k in range(token_size)])
#             print(f"チャンク{j}: {surface}, 係り先: {chunk.link}")
            
#             node = pydot.Node(surface)
#             graph.add_node(node)
#             nodes.append((node, chunk.link))
            
#         for j, (node, link) in enumerate(nodes):
#             if link != -1 and link < len(nodes):
#                 graph.add_edge(pydot.Edge(node, nodes[link][0]))
                
#         graph.write_png(f'output44_sentence{i+1}.png')
        
#         # 画像表示
#         img = mpimg.imread(f'output44_sentence{i+1}.png')
#         plt.figure(figsize=(12, 8))
#         plt.imshow(img)
#         plt.axis('off')
#         plt.title(f'係り受け木: 文{i+1}')
#         plt.show()
