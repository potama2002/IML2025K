from knock30 import parse_mecab_result

if __name__ == "__main__":
    sentences = parse_mecab_result("merosu.txt.mecab")
    max_noun_phrase = ''
    
    for sentence in sentences:
        chunk = []
        for morph in sentence:
            if morph['pos'] == '名詞':
                chunk.append(morph['surface'])
            else:
                if len(chunk) >= 2:
                    phrase = ''.join(chunk)
                    if len(phrase) > len(max_noun_phrase):
                        max_noun_phrase = phrase
                chunk = []
        if len(chunk) >= 2:
            phrase = ''.join(chunk)
            if len(phrase) > len(max_noun_phrase):
                max_noun_phrase = phrase

    print(max_noun_phrase)
