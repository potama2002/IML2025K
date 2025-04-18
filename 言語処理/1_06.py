def ngram(sentence,n):
    
    return [sentence[idx:idx+n]for idx in range(len(sentence)-n+1)]

word1='paraparaparadise'
word2='paragraph'

X=set(ngram(word1,2))
Y=set(ngram(word2,2))
print("X=",X)
print("Y=",Y)
print("和集合",X|Y)
print("積集合",X&Y)
print("差集合",X-Y)

print('se' in X)
print('se' in Y)

