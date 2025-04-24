import CaboCha

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

def extract_dependencies(text):
    c = CaboCha.Parser()
    tree = c.parse(text)
    lines = tree.toString(CaboCha.FORMAT_LATTICE).splitlines()

    dependencies = []
    chunks = {}
    chunk_dst = {}

    # Process each line from CaboCha output
    current_chunk_id = None
    for line in lines:
        if line.startswith("*"):  # Chunk line
            parts = line.split()
            current_chunk_id = int(parts[1])
            dst = int(parts[2].strip("D"))
            chunk_dst[current_chunk_id] = dst
            chunks[current_chunk_id] = []  # Initialize the chunk's token list
        elif "\t" in line:  # Token line
            token_surface = line.split("\t")[0]
            if current_chunk_id is not None:
                chunks[current_chunk_id].append(token_surface)

    # Build dependency pairs
    for src_chunk_id, dst_chunk_id in chunk_dst.items():
        if dst_chunk_id != -1:  # Skip root nodes
            src_tokens = "".join(chunks[src_chunk_id])
            dst_tokens = "".join(chunks[dst_chunk_id])
            dependencies.append(f"{src_tokens}\t{dst_tokens}")

    return dependencies

dependencies = extract_dependencies(text)
print("係り元と係り先 (タブ区切り形式):")
for dep in dependencies:
    print(dep)

'''
＜実行結果
係り元と係り先 (タブ区切り形式):
メロスは	激怒した。
激怒した。	決意した。
必ず、	除かなければならぬと
かの	邪智暴虐の
邪智暴虐の	王を
王を	除かなければならぬと
除かなければならぬと	決意した。
決意した。	わからぬ。
メロスには	わからぬ。
政治が	わからぬ。
わからぬ。	牧人である。
メロスは、	牧人である。
村の	牧人である。
牧人である。	暮して来た。
笛を	吹き、
吹き、	暮して来た。
羊と	遊んで
遊んで	暮して来た。
暮して来た。	敏感であった。
けれども	敏感であった。
邪悪に対しては、	敏感であった。
人一倍に	敏感であった。
'''