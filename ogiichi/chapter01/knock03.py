'''
“Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.”
という文を単語に分解し、各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ。

実行結果
['Now', 'I', 'need', 'a', 'drink,', 'alcoholic', 'of', 'course,', 'after', 'the', 'heavy', 'lectures', 'involving', 'quantum', 'mechanics.']
'''

str = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'

words = []

words = str.split()

print(words)