import CaboCha

text = "メロスは激怒した。"

def visualize_dependency_tree(text):
    c = CaboCha.Parser()
    tree = c.parseToString(text)
    print(tree)

visualize_dependency_tree(text)

'''
＜実行結果＞
  メロスは-D
  激怒した。
EOS
'''