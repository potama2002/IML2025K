import MeCab
import CaboCha

def text_visualize_dependency_tree(sentence):
    parser = CaboCha.Parser()
    tree = parser.parse(sentence)
    
    # 各文節のテキストとその係り先を抽出
    chunks = []
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_text = ""
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            chunk_text += token.surface
        chunks.append({
            'id': i,
            'text': chunk_text,
            'link': chunk.link
        })
    
    # テキストベースの木構造を作成
    print(f"文: {sentence}")
    print("\n係り受け構造:")
    
    # ルート（文末）の文節を特定
    root_id = None
    for i, chunk in enumerate(chunks):
        if chunk['link'] == -1:
            root_id = i
            break
    
    # 再帰的に木構造を表示する関数
    def print_tree(node_id, depth=0):
        prefix = "  " * depth
        chunk = chunks[node_id]
        if depth > 0:
            print(f"{prefix}└─ {chunk['text']}")
        else:
            print(f"{prefix}{chunk['text']}")
        
        # この文節に係る文節を探す
        children = [i for i, c in enumerate(chunks) if c['link'] == node_id]
        for child in children:
            print_tree(child, depth + 1)
    
    # ルートから表示開始
    if root_id is not None:
        print_tree(root_id)

# 例文の係り受け木をテキストで可視化
text_visualize_dependency_tree("メロスは激怒した。")