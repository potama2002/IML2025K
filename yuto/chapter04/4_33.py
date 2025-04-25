import MeCab
import CaboCha

text = '''メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。'''

def improved_dependency_parse(text):
    # 文単位で分割
    sentences = [s + '。' for s in text.split('。') if s.strip()]
    
    parser = CaboCha.Parser()
    all_dependencies = []
    
    # 各文ごとに解析
    for i, sentence in enumerate(sentences):
        tree = parser.parse(sentence)
        
        # 文番号を追加して表示
        print(f"\n【文{i+1}】 {sentence}")
        
        dependencies = []
        for j in range(tree.chunk_size()):
            chunk = tree.chunk(j)
            dep_pos = chunk.link
            
            if dep_pos >= 0:
                # 係り元の文節のテキストを取得
                source_text = ""
                for k in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                    token = tree.token(k)
                    source_text += token.surface
                
                # 係り先の文節のテキストを取得
                target_text = ""
                target_chunk = tree.chunk(dep_pos)
                for k in range(target_chunk.token_pos, target_chunk.token_pos + target_chunk.token_size):
                    token = tree.token(k)
                    target_text += token.surface
                
                dependencies.append((source_text, target_text))
        
        all_dependencies.extend(dependencies)
    
    return all_dependencies

deps = improved_dependency_parse(text)
for src, dst in deps:
    print(f"{src}\t→\t{dst}")