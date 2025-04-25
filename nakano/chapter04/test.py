

import CaboCha

parser = CaboCha.Parser()
sentence = "太郎はこの本を二郎を見た女性に渡した。"
print(parser.parseToString(sentence))

