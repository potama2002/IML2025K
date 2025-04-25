import CaboCha

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

def extract_predicates_with_subject(text, subject="メロス"):
    c = CaboCha.Parser()
    tree = c.parse(text)
    lines = tree.toString(CaboCha.FORMAT_LATTICE).splitlines()

    chunks = {}
    chunk_dst = {}
    current_chunk_id = None

    # Parse chunks and tokens
    for line in lines:
        if line.startswith("*"):  # Chunk line
            parts = line.split()
            current_chunk_id = int(parts[1])
            dst = int(parts[2].strip("D"))
            chunk_dst[current_chunk_id] = dst
            chunks[current_chunk_id] = []  # Initialize the chunk
        elif "\t" in line:  # Token line
            token_surface = line.split("\t")[0]
            if current_chunk_id is not None:
                chunks[current_chunk_id].append(token_surface)

    predicates = []
    for src_chunk_id, dst_chunk_id in chunk_dst.items():
        if dst_chunk_id != -1:  # Skip root nodes
            src_tokens = "".join(chunks[src_chunk_id])
            dst_tokens = "".join(chunks[dst_chunk_id])

            # Check if the source contains the subject (e.g., "メロス")
            if subject in src_tokens:
                # The destination chunk often contains the predicate
                predicates.append(dst_tokens)

    return predicates

predicates = extract_predicates_with_subject(text, subject="メロス")
print(f"「メロス」が主語のときの述語:")
for predicate in predicates:
    print(predicate)

'''
＜実行結果＞
「メロス」が主語のときの述語:
激怒した。
わからぬ。
牧人である。
'''