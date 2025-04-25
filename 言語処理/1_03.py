#coding: utf-8
sentence='Now I need a drink, alcoholic of course, after the heavy lectures involving quantum'
result=[]

words=sentence.split(' ')
for word in words:
    result.append(len(word)-word.count(',')-word.count('.'))
                  
print(result)