str = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
l = str.replace(",","").replace(".", "").split(" ")
pi = []
for i in range(len(l)):
    pi.append(len(l[i]))
print(pi)