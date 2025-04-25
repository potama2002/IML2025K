import MeCab

text = '''メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。'''

def extract_noun_phrases(text):
    tagger = MeCab.Tagger()
    #形態素解析情報取得
    node=tagger.parseToNode(text)
    #形態素
    morphemes=[]
    
    while node:
        if node.surface:
            features=node.feature.split(',')
            pos=features[0]if features else ""
            morphemes.append((node.surface,pos))
        node=node.next
    #ここで名詞抽出
    phrases=[]
    for i in range(1,len(morphemes)-1):
        if(morphemes[i-1][1]=='名詞'and
           morphemes[i][0]=='の'and morphemes[i][1]=='助詞'and
           morphemes[i+1][1]=='名詞'):
            phrases.append(f"{morphemes[i-1][0]}の{morphemes[i+1][0]}")
    return phrases

noun_phrases = extract_noun_phrases(text)
print("「AのB」形式の名詞句:", noun_phrases)