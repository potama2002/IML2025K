import MeCab
import CaboCha

text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""


A = MeCab.Tagger()

result = A.parse(text)
    # 行に分割
lines = result.split('\n')

print()
print("--- 33 ---")
print()

def extract_dependencies(text):
    # CaboChaパーサーの初期化
    parser = CaboCha.Parser()

    # 解析
    tree = parser.parse(text)

    # 結果を保存するリスト
    results = []

    # 文節（チャンク）の数
    chunk_size = tree.chunk_size()

    # 各文節を処理
    for i in range(chunk_size):
        chunk = tree.chunk(i)
        head_pos = chunk.link  # 係り先ID

        # 現在の文節の文字列を取得
        begin = chunk.token_pos
        end = chunk.token_pos + chunk.token_size
        from_text = ''.join([tree.token(j).surface for j in range(begin, end)])

        # 係り先の文字列を取得
        if head_pos != -1:
            to_begin = tree.chunk(head_pos).token_pos
            to_end = to_begin + tree.chunk(head_pos).token_size
            to_text = ''.join([tree.token(j).surface for j in range(to_begin, to_end)])
            results.append(f"{from_text}\t{to_text}")
        else:
            results.append(f"{from_text}\t文末")

    return results

# 使用例
for dep in extract_dependencies(text):
    print(dep)