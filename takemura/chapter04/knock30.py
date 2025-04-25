def parse_mecab_result(filepath):
    sentences = []
    sentence = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line == 'EOS\n':
                if sentence:  # 空でない場合のみ追加
                    sentences.append(sentence)
                    sentence = []
                continue
            if '\t' not in line:
                continue
            surface, others = line.strip().split('\t')
            parts = others.split(',')
            morph = {
                'surface': surface,
                'base': parts[6],
                'pos': parts[0],
                'pos1': parts[1]
            }
            sentence.append(morph)
    return sentences

# 実行テスト
if __name__ == "__main__":
    result = parse_mecab_result('merosu.txt.mecab')
    for morph in result[0]:  # 最初の文だけ確認
        print(morph)
