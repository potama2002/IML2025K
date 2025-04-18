from knock05 import n_gram


word00 = "paraparaparadise"
word01 = "paragraph"


# 集合X
set_X:list = n_gram(word00, 2)
set_X = set(set_X)  #setにすると重複が削除されるので集合になる．literally
print("elements of set X: ",set_X)
# 集合Y
set_Y:list = n_gram(word01, 2)
set_Y = set(set_Y)
print("elements of set Y: ",set_Y)

print("\nResults:" )

# 和集合
set_union = set_X | set_Y
print("union: ",set_union)

# 差集合
set_diff = set_X - set_Y
print("difference: ",set_diff)

# 積集合
set_intersection = set_X & set_Y
print("intersection: ",set_intersection)

# Xに"se"が含まれるか
set_X_has_se:bool = "se" in set_X
print("X has 'se': ",set_X_has_se)

# reference: https://qiita.com/Tadataka_Takahashi/items/10818c1eac8225a68de8
