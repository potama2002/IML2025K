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

print()
print("--- 30 ---")
print()

A = MeCab.Tagger()

result = A.parse(text)
    # 行に分割
lines = result.split('\n')

# 動詞を抽出
verbs = []
for line in lines:
    if line == 'EOS' or line == '':
        continue

    # タブで分割して表層形と品詞情報を取得
    parts = line.split('\t')
    if len(parts) < 2:
        continue

    surface = parts[0]
    features = parts[1].split(',')

    # 品詞が動詞の場合のみ追加
    if features[0] == '動詞':
        verbs.append({ surface,  # 表層形（活用形）
        })
# print(result)
print(verbs)


print()
print("--- 31 ---")
print()
verbs = []
for line in lines:
    if line == 'EOS' or line == '':
        continue

    # タブで分割して表層形と品詞情報を取得
    parts = line.split('\t')
    if len(parts) < 2:
        continue

    surface = parts[0]
    features = parts[1].split(',')

    # 品詞が動詞の場合のみ追加
    if features[0] == '動詞':
        verbs.append({
        'surface': surface,  # 表層形（活用形）
        'base': features[6] if len(features) > 6 else surface,  # 原形（基本形）
        })
print(verbs)

print()
print("--- 32 ---")
print()

morphemes = []
for line in lines:
    if line == 'EOS' or line == '':
        continue

    # タブで分割して表層形と品詞情報を取得
    parts = line.split('\t')
    if len(parts) < 2:
        continue

    surface = parts[0]
    features = parts[1].split(',')

    # 形態素情報を辞書として保存
    morpheme = {
        'surface': surface,
        'pos': features[0],
        'pos1': features[1] if len(features) > 1 else ''
    }
    
    morphemes.append(morpheme)

# 「名詞+の+名詞」のパターンを抽出
noun_no_noun_phrases = []
for i in range(len(morphemes) - 2):
    # 名詞+の+名詞のパターンを検出
    if (morphemes[i]['pos'] == '名詞' and 
        morphemes[i+1]['surface'] == 'の' and morphemes[i+1]['pos'] == '助詞' and 
        morphemes[i+2]['pos'] == '名詞'):
        
        phrase = morphemes[i]['surface'] + morphemes[i+1]['surface'] + morphemes[i+2]['surface']
        noun_no_noun_phrases.append(phrase)
print(noun_no_noun_phrases)

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

print()
print("--- 34 ---")
print()
nodes = A.parseToNode(text)
# 形態素分解した文字の数だけ、情報の文字列を「,」で分割して
# 名詞のときだけ表層形を表示しつづける
found_Melos = False
while nodes:
    features = nodes.feature.split(',')
    pos = features[0]
    if pos == '名詞' and nodes.surface == 'メロス':
        found_Melos = True
        # print(nodes.surface)
    elif found_Melos and pos == '動詞':
        base_form = features[6] if len(features) > 6 else nodes.surface
        print(f"述語: {nodes.surface}（基本形: {base_form}）")
        # 一つの述語を見つけたらフラグをリセット（次の主語-述語ペアを探すため）
        found_Melos = False

    # 助詞「は」「が」などが来たらフラグをリセット（主語が違う文に移った可能性）
    elif found_Melos and pos == '助詞' and nodes.surface in ['は', 'が']:
        found_Melos = False
    nodes = nodes.next