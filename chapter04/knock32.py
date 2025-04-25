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