data = "stressed"
reverse = ""

#   1.逆カウントのループ
i = len(data) - 1
while i >= 0:
    reverse += data[i]
    i-=1
print(reverse)

