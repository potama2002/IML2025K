import MeCab

text = '''メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。'''

def extract_verbs(text):
    tagger=MeCab.Tagger()
    node=tagger.parseToNode(text)
    verb_bases=[]
    while node:
        features=node.feature.split(',')
        if features[0]=='動詞':
            if len(features)>6:
                verb_bases.append((node.surface,features[6]))
        node=node.next
    return verb_bases
verb_bases=extract_verbs(text)
for verb,base in verb_bases:
    print(f"{verb}->{base}")
