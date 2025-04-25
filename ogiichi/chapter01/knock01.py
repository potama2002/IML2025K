'''
文字列「パタトクカシーー」の2, 4, 6, 8文字目を取り出し、それらを連結した文字列を得よ。

実行結果
タクシー
'''

str = 'パタトクカシーー'
result = ''

for i in range(len(str)):
    if (i%2 == 1):
        result += str[i]

print(result)