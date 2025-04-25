import MeCab

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

# テキストを解析
nodes = tagger.parseToNode(text)

# メロスが主語の時の述語を抽出
print("「メロス」が主語である述語:")
found_Melos = False
subject_marker = None  # 主語を示す助詞（「は」や「が」など）を保存

while nodes:
    # ノードの表層形と品詞情報を取得
    surface = nodes.surface
    features = nodes.feature.split(',')
    pos = features[0]  # 品詞

    # メロスという名詞を見つけた場合
    if pos == '名詞' and surface == 'メロス':
        found_Melos = True
        subject_marker = None  # 助詞はまだ見つかっていない

    # メロスの後に助詞「は」「が」などが来た場合、それを記録
    elif found_Melos and pos == '助詞' and surface in ['は', 'が', 'も']:
        subject_marker = surface

    # 助詞が見つかった後に動詞が来た場合、それを述語として抽出
    elif found_Melos and subject_marker and pos == '動詞':
        base_form = features[6] if len(features) > 6 else surface
        print(f"メロス{subject_marker} {surface}（基本形: {base_form}）")

        # 文末まで追跡して、述語の完全な形を取得
        predicate_parts = [surface]
        next_node = nodes.next
        while next_node:
            next_features = next_node.feature.split(',')
            next_pos = next_features[0]

            # 文の区切りを見つけたら終了
            if next_node.surface in ['。', '！', '？', '\n'] or next_pos == '記号':
                break

            # 助動詞や接続助詞なども述語の一部として扱う
            if next_pos in ['助動詞', '助詞'] or (next_pos == '動詞' and next_features[1] == '非自立'):
                predicate_parts.append(next_node.surface)
            else:
                break

            next_node = next_node.next

        if len(predicate_parts) > 1:
            print(f"完全な述語: {''.join(predicate_parts)}")
        print("---")

        # 一つの述語を見つけたらフラグをリセット（次の主語-述語ペアを探すため）
        found_Melos = False
        subject_marker = None

    # 新しい文が始まったらフラグをリセット
    elif surface in ['。', '！', '？', '\n']:
        found_Melos = False
        subject_marker = None

    nodes = nodes.next

"""
「メロス」が主語である述語:
メロスは し（基本形: する）
完全な述語: した
---
メロスが わから（基本形: わかる）
完全な述語: わからぬ
---
"""