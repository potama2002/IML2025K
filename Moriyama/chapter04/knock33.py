import spacy

# 正しいディレクトリパスを指定！
nlp = spacy.load("ja_ginza-5.2.0/ja_ginza/ja_ginza-5.2.0")
#spaCy: 自然言語処理ライブラリ　文構造、係り受けの解析が得意
#GINZA: spaCy対応の日本語モデル
text = """
メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。
"""

doc = nlp(text) #トークン化＋品詞解析＋係り受け解析

for token in doc:
    print(f"{token.text}\t{token.head.text}\t{token.dep_}")

# token.text: 単語そのもの（表層系）
# token.head.text: その単語の係り先
# token.dep_: 単語と係り先の関係
"""
| ラベル     | 意味（日本語）       | 例文内での役割例                             |
|------------|----------------------|----------------------------------------------|
| ROOT       | 文の中心（述語）     | 文のメイン動詞（例：激怒**した**）         |
| nsubj      | 主語（名詞主語）     | **メロス** は激怒した                        |
| obj        | 目的語               | りんごを**食べた** → りんごが `obj`         |
| iobj       | 間接目的語           | 彼に**花をあげた** → 彼が `iobj`            |
| obl        | 副詞句修飾語         | 学校に**行った** → 学校にが `obl`          |
| advmod     | 副詞修飾語           | **必ず**激怒した                             |
| amod       | 形容詞修飾語         | **美しい**花                                 |
| aux        | 助動詞               | 怒っ**た**、食べ**ない**（「た」「ない」）  |
| mark       | 接続助詞             | 〜**ば**、〜**ので**など                     |
| case       | 格助詞               | は、が、を、に、の（名詞に係る）            |
| cc         | 接続詞               | A**と**B、A**や**B                           |
| conj       | 並列要素             | Aと**B** → Bが `conj`                        |
| compound   | 名詞の複合語         | **邪智暴虐**の王 → 邪智が暴虐に `compound`  |

"""
"""実行結果
        メロス  compound
メロス  激怒    nsubj
は      メロス  case
激怒    激怒    ROOT
し      激怒    aux
た      激怒    aux
。      激怒    punct


        ROOT
必ず    除か    advmod
、      必ず    punct
かの    暴虐    det
邪智    暴虐    compound
暴虐    王      nmod
の      暴虐    case
王      除か    obj
を      王      case
除か    決意    advcl
なけれ  除か    aux
ば      なけれ  fixed
なら    なけれ  fixed
ぬ      なけれ  fixed
と      除か    case
決意    決意    ROOT
し      決意    aux
た      決意    aux
。      決意    punct

        メロス  compound
メロス  わから  obl
に      メロス  case
は      メロス  case
政治    わから  nsubj
が      政治    case
わから  わから  ROOT
ぬ      わから  aux
。      わから  punct

        メロス  compound
メロス  牧人    nsubj
は      メロス  case
、      メロス  punct
村      牧人    nmod
の      村      case
牧人    牧人    ROOT
で      牧人    cop
ある    で      fixed
。      牧人    punct

        笛      compound
笛      吹き    obj
を      笛      case
吹き    暮し    advcl
、      吹き    punct
羊      遊ん    obl
と      羊      case
遊ん    暮し    advcl
で      遊ん    mark
暮し    暮し    ROOT
て      暮し    mark
来      て      fixed
た      暮し    aux
。      暮し    punct

        邪悪    obl
けれど
        case
も
        case
邪悪    敏感    obl
に      邪悪    case
対し    に      fixed
ては    に      fixed
、      邪悪    punct
人      倍      compound
一      倍      nummod
倍      敏感    obl
に      倍      case
敏感    敏感    ROOT
で      敏感    aux
あっ    で      fixed
た      敏感    aux
。      敏感    punct

"""