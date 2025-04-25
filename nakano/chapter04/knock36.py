#!/usr/bin/env python3
# coding: utf-8

import json
from collections import Counter
import MeCab

def parse_wikipedia_corpus(file_path: str):
    '''
    単語（トークン）の出現頻度が高い上位20語を表示する
    '''
    mecab = MeCab.Tagger("-Ochasen")
    counter = Counter()
    '''
    collection.Counterは、要素の出現回数をカウントするための辞書のサブクラス
    例えば、Counter(['a', 'b', 'c', 'a', 'b', 'b'])は
    {'a': 2, 'b': 3, 'c': 1}のような辞書を作成する
    
    '''

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f: # 各行は1記事→1記事ごとに処理する
            article = json.loads(line) # load an article
            text = article['text'] #　記事本文を取得
            node = mecab.parseToNode(text)
            '''
            [ノード①：「私」] → [ノード②：「は」] → [ノード③：「パン」] → [ノード④：「を」] → [ノード⑤：「食べ」] → [ノード⑥：「ます」] → [ノード⑦：「。」] → [終端ノード]
            こんな感じのノードの連結を作成する．
            以下でグラフを探索する
            探索の様子
            node→BOS（空）→「私」→「は」→「パン」→「を」→「食べ」→「ます」→「。」→EOS（空）→終了



            '''

            while node:# node = トークン（単語）ごと
                surface = node.surface.strip()
                if surface:
                    counter[surface] += 1 # つまり文中に出てくる表現に対してそのカウントを1つインクリメントする
                node = node.next
    return counter.most_common(20) # 便利．上位20個を取得する

if __name__ == "__main__":
    freq = parse_wikipedia_corpus('jawiki-country.json')
    print("頻出上位20単語:")
    for word, count in freq:
        print(f"{word}\t{count}")



'''
36. 単語の出現頻度
問題36から39までは、Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzをコーパスと見なし、統計的な分析を行う。
1行に1記事の情報がJSON形式で格納される
各行には記事名が”title”キーに、記事本文が”text”キーの辞書オブジェクトに格納され、そのオブジェクトがJSON形式で書き出される
ファイル全体はgzipで圧縮される
まず、第3章の処理内容を参考に、Wikipedia記事からマークアップを除去し、各記事のテキストを抽出せよ。そして、コーパスにおける単語（形態素）の出現頻度を求め、出現頻度の高い20語とその出現頻度を表示せよ。

'''
'''
jsonの形式
- 1行に1記事

例）
{"title": "エジプト", "text": "{{otheruses|主に現代のエジプト・アラブ共和国|古代|古代エジプト}}\n{{基礎情報 国\n|略名 =エジプト\n|漢字書き=埃及\n|日本語国名 =エジプト・アラブ共和国\n|公式国名 ={{lang|ar|
''جمهورية مصر العربية''}}\n|国旗画像 =Flag of Egypt.svg\n|国章画像 =[[ファイル:Coat_of_arms_of_Egypt.svg|100px|エジプトの国章]]\n|国章リンク =（[[エジプトの国章|国章]]）\n|標語 =なし\n|位置画像 =Egypt (orthographic projection).svg\n|公用語 =[[アラビア語]]\n|首都 =[[File:Flag of Cairo.svg|24px]] [[カイロ]]\n|最大都市 =カイロ\n|元首等肩書 =[[近代エジプトの国家元首の一覧|大統領]]\n|元首等氏名 =[[アブドルファッターフ・アッ＝シーシー]]\n|首相等肩書 ={{ill2|エジプトの首相|en|Prime Minister of Egypt|label=首相}}\n|首相等氏名 ={{仮リンク|ムスタファ・マドブーリー|ar|مصطفى مدبولي|en|Moustafa Madbouly}}\n|面積順位 =29\n|面積大きさ =1 E12\n|面積値 =1,010,408\n|水面積率 =0.6%\n|人口統計年 =2012\n|人口順位 =\n|人口大

こんな感じなのでtextだけ抽出する



'''