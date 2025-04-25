import MeCab
import CaboCha

text = '''メロスは激怒した。
必ず、かの邪智暴虐の王を除かなければならぬと決意した。
メロスには政治がわからぬ。
メロスは、村の牧人である。
笛を吹き、羊と遊んで暮して来た。
けれども邪悪に対しては、人一倍に敏感であった。'''

def extract_melos_predicates(text):
    parser = CaboCha.Parser()
    
    # 文単位で分割
    sentences = [s + '。' for s in text.split('。') if s.strip()]
    
    melos_predicates = []
    
    for sentence in sentences:
        tree = parser.parse(sentence)
        
        # 「メロス」を含む文節を探す
        melos_chunk_id = -1
        for i in range(tree.chunk_size()):
            chunk = tree.chunk(i)
            chunk_text = ""
            for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                token = tree.token(j)
                chunk_text += token.surface
            
            # 「メロス」を含む文節を見つけたら
            if "メロス" in chunk_text:
                # 助詞「は」「が」などがあるか確認（主語の特徴）
                has_subject_marker = False
                for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                    token = tree.token(j)
                    if token.feature.split(',')[0] == '助詞' and token.surface in ['は', 'が', 'には']:
                        has_subject_marker = True
                        break
                
                if has_subject_marker:
                    melos_chunk_id = i
                    break
        
        # 「メロス」を主語とする文節が見つかった場合
        if melos_chunk_id >= 0:
            chunk = tree.chunk(melos_chunk_id)
            if chunk.link >= 0:  # 係り先がある
                # 係り先（述語）の文節を取得
                pred_chunk = tree.chunk(chunk.link)
                pred_text = ""
                for j in range(pred_chunk.token_pos, pred_chunk.token_pos + pred_chunk.token_size):
                    token = tree.token(j)
                    pred_text += token.surface
                
                # 述語を追加
                melos_predicates.append(pred_text)
    
    return melos_predicates

predicates = extract_melos_predicates(text)
print("「メロス」が主語のときの述語:")
for pred in predicates:
    print(f"- {pred}")