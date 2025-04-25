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