import random

# Typoglycemia


def typoglycemia(sentence):
    words = sentence.split()
    #print(type(words)) split()の結果はリストらしい
    result = []
    
    if len(words) >4:
        # 先頭と末尾を除いた部分をシャッフル
        middle = list(words[1:-1])
        random.shuffle(middle)
        words[1:-1] = middle
    out = " ".join(words)
    return out

    #for w in words:
    #    # 長さが5文字以上なら，先頭と末尾以外をシャッフル
    #    if len(w) > 4:
    ##        middle = list(w[1:-1])
    #        random.shuffle(middle)
    #        w = w[0] + "".join(middle) + w[-1]
    #    result.append(w)
    #return " ".join(result)

text = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print(typoglycemia(text))


