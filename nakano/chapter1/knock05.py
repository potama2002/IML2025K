
# 参考：https://qiita.com/kazmaw/items/4df328cba6429ec210fb

def n_gram(target:str, n:int)-> list:
  # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
  return [ target[idx:idx + n] for idx in range(len(target) - n + 1)]

target = "I am an NLPer"




if __name__ == "__main__":
    # print(n_gram(target, 1))
    # > ['I', ' ', 'a', 'm', ' ', 'a', 'n', ' ', 'N', 'L', 'P', 'e', 'r']
    print("bi-gram")
    print(n_gram(target, 2))
    # > ['I ', ' a', 'am', 'm ', ' a', 'an', 'n ', ' N', 'NL', 'LP', 'Pe', 'er']
    print("tri-gram1")
    print(n_gram(target, 3))
    # > ['I a', ' am', 'am ', 'm a', ' an', 'an ', 'n N', ' NL', 'NLP', 'LPe', 'Per']

    #words = target.split(' ')
    #print(n_gram(words, 1))
    # > [['I'], ['am'], ['an'], ['NLPer']]
    #print(n_gram(words, 2))
    # > [['I', 'am'], ['am', 'an'], ['an', 'NLPer']]
    #print(n_gram(words, 3))
    # > [['I', 'am', 'an'], ['am', 'an', 'NLPer']]


