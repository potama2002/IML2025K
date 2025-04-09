def ngram(s,n):
    return [s[idx:idx+n]for idx in range(len(s)-n+1)]

s='I am an NLPer'
print(ngram(s,3))

word=s.split(' ')
print(ngram(s,1))



