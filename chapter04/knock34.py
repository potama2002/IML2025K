from knock30 import parse_mecab_result

if __name__ == "__main__":
    sentences = parse_mecab_result("merosu.txt.mecab")
    for sentence in sentences:
        chunk = []  # 名詞が続いている部分を一時保存
        for morph in sentence:
            if morph['pos'] == '名詞':
                chunk.append(morph['surface'])
            else:
                if len(chunk) >= 2:
                    print(''.join(chunk))  # 連続していたら出力
                chunk = []  # 名詞以外が来たらリセット
        # 文末にも名詞連続があるかもしれないのでチェック
        if len(chunk) >= 2:
            print(''.join(chunk))
