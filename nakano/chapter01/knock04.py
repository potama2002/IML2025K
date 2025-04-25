
sentence = ("Hi He Lied Because Boron Could Not Oxidize Fluorine. "
            "New Nations Might Also Sign Peace Security Clause. "
            "Arthur King Can.")
sentence = sentence.replace('.', '')
words = sentence.split()

# 1文字を取り出す単語
one_char_indices = [1, 5, 6, 7, 8, 9, 15, 16, 19]

element_dict = {}
for i, word in enumerate(words, start=1):
    if i in one_char_indices:
        element_dict[word[:1]] = i
    else:
        element_dict[word[:2]] = i

print(element_dict)

