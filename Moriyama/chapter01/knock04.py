

def extWord(i, word):
  if i in [1,5,6,7,8,9,15,16,19]:
    return (word[0], i)
  else:
    return (word[:2], i)

str = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
text = str.replace('.', '').replace(',' '')
ans = []

ans = [extWord(i, w) for i, w in enumerate(text.split())]

ans = []
for i, w in enumerate(text.split()):
  ans.append = extWord(i, w)
