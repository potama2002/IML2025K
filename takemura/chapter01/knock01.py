text1 = "パトカー"
text2 = "タクシー"

ansText = ""
ansText2 = ""

for i in range(len(text1)):
   ansText += text1[i]
   ansText += text2[i]

print(ansText)

for j in range(len(text2)):
   ansText2 += ansText[j*2+1]

print(ansText2)