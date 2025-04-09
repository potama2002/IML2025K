# 00
str_1 = "パトカー"
str_2 = "タクシー"
out = ""
for i in range(len(str_1) or len(str_2)):
    out += str_1[i]
    out += str_2[i]
print(out)


# 01
index = [2, 4, 6, 8]
out_2 = ""

for i in index:
    out_2 +=out[i-1]

print(out_2)


# 02
str_3 = "stressed"
print(len(str_3))
out_3 = ""

for i in range(len(str_3)):
    out_3 += str_3[7 - i]

print(out_3)


#  03
str_4 = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
splitted = str_4.split()
out_4 = []

for i in range(len(splitted)):
    word = splitted[i]
    out_4.append(len(word))

print(out_4)

# 04
str_5 = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
Single_char_indexes = [1, 5, 6, 7, 8, 9, 15, 16, 19]
out_5 = {}
key = ""

splitted = str_5.split()
for i in range(len(splitted)):
    if (i+1) in Single_char_indexes:
        key = splitted[i][:2]
    else:
        key = splitted[i][:1]
    out_5[key] = (i+1)

print(out_5)


# 05
print("")
print("05")
print("")
def n_gram(word, n):
    n_grams = []
    for i in range(len(word) - n + 1):
     n_grams.append(word[i:i+n])
    return n_grams

str_6 = "I am an NLPer"
tri_gram = n_gram(str_6, 2)

splitted = str_6.split()
bi_gram = n_gram(splitted, 2)

print(tri_gram)
print(bi_gram)


# 06
print("")
print("06")
print("")
par_1 = "paraparaparadise"
par_2 = "paragraph"

X = n_gram(par_1, 2)
Y = n_gram(par_2, 2)
XY_sum = []
XY_int = []
XY_sub = []

XY_sum = X + Y
for i in range(len(X) or len(Y)):
    if X[i] in Y:
        if X[i] not in XY_int:
            XY_int.append(X[i])

for i in range(len(X)):
    if X[i] not in XY_int:
        XY_sub.append(X[i])

print(XY_sum)
print(XY_int)
print(XY_sub)

# 07
print("")
print("07")
print("")

def make_str(x, y, z):
    return f"{x}時のときの{y}は{z}"

print(make_str(12, "気温", 22.4))

# 08
print("")
print("08")
print("")

def cipher(sentence):
    chars = list(sentence)
    out = ""
    for i in range(len(chars)):
        if ord(chars[i]) >= 97 and ord(chars[i]) <= 127:
            chars[i] = chr(219 - ord(chars[i]))
        out += chars[i]
    return out

cipherd = (cipher("Hello"))
print(cipherd)
original = cipher(cipherd)
print(original)


# 09
import random

str_9 = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind."

splitted = str_9.split()
out  = ""
for i in range(len(splitted)):
    length = len(splitted[i])
    if length > 4:
        lst = list(range(1, length))
        indexes = (random.sample(lst, len(lst)))
        for j in range(len(indexes)):
            splitted[j] = splitted[index[j]]

print()
