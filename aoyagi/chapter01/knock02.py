text="Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

words=text.replace(',', '').replace('.', '').split()
lengths = [len(word) for word in words]
print(lengths)