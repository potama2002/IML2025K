str1 = "パトカー"
str2 = "タクシー"
pataxList = list()

for patr, taxi in zip(list(str1),list(str2)):
    pataxList.append(patr)
    pataxList.append(taxi)
str3 = ''.join(pataxList)


result = str3[1] + str3[3] + str3[5] + str3[7]
print(result)