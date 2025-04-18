def ngram(sentence,n):
    
    return [sentence[idx:idx+n]for idx in range(len(sentence)-n+1)]

sentence="I am an NLPer"
print(ngram(sentence,1))
print(ngram(sentence,2))
print(ngram(sentence,3))

word=sentence.split(' ')
print(ngram(word,1))
print(ngram(word,2))
print(ngram(word,3))


