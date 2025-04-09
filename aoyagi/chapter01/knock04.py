def n_gram(sequence,n):
    return [target[idx:idx+n] for idx in range(len(target)-n+1)]

target="I am an NLPer"
print(n_gram(target,1))
print(n_gram(target,2))
print(n_gram(target,3))

words=target.split('')
print(n_gram(words,1))
print(n_gram(words,2))
print(n_gram(words,3))