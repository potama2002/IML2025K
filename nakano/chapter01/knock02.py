
word="stressed"

result=""
for i in range(len(word)-1,-1,-1):
    result += word[i]

print(result)  # desserts

# or
result = word[::-1]  #これでもいけるっぽい
print(result)  # desserts