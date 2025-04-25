'''
与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ。
この関数を用い、”I am an NLPer”という文から文字tri-gram、単語bi-gramを得よ。

実行結果
['I', 'a', 'm', 'a', 'n', 'N', 'L', 'P', 'e', 'r']
['I', 'am', 'an', 'NLPer']
'''

def tri_gram(str):
    result = []
    for s in str:
        if not ' ' in s:
            result += s
    
    return result

def bi_gram(str):
    result = []
    result = str.split()

    return result

str = 'I am an NLPer'
result1 = tri_gram(str)
result2 = bi_gram(str)
print(result1)
print(result2)