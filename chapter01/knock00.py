str1 = "パトカー"
str2 = "タクシー"
pataxList = list()

for patr, taxi in zip(list(str1),list(str2)):
    pataxList.append(patr)
    pataxList.append(taxi)

print(''.join(pataxList))

git branch Moriyama
git checkout Moriyama
git add ./Moriyama/chapter01/knock01.py
git add ./Moriyama/chapter03/
git commit -m "your message"
git pull origin main
git push origin Moriyama