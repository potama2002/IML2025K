'''
2つの文字列「パトカー」と「タクシー」の文字を先頭から交互に連結し、文字列「パタトクカシーー」を得よ。

実行結果
パタトクカシーー
'''

str1 = 'パトカー'
str2 = 'タクシー'
result = ''

for i in range(4):
    result += str1[i] + str2[i]

print(result)