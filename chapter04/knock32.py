from knock30 import parse_mecab_result  # 30番の関数を再利用

if __name__ == "__main__":
    sentences = parse_mecab_result("merosu.txt.mecab")
    for sentence in sentences:
        for morph in sentence:
            if morph['pos'] == '動詞':
                print(morph['base'])
