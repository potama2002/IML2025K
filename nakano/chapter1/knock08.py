def cipher(text):
    result = []
    for c in text:
        if c.islower():  # 英小文字判定
            # 文字コードを219 - ord(c)に変換
            result.append(chr(219 - ord(c)))
        else:
            # そのまま
            result.append(c)
    return "".join(result)

message = "I love Python 3.8!"
encrypted = cipher(message)
decrypted = cipher(encrypted)

print("Original :", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
