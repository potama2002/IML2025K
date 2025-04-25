from knock30 import parse_mecab_result

if __name__ == "__main__":
    sentences = parse_mecab_result("merosu.txt.mecab")
    for sentence in sentences:
        for morph in sentence:
            if morph['pos'] == '名詞' and morph['pos1'] == 'サ変接続':
                print(morph['surface'])
