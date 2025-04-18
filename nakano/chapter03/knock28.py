import re
from typing import Dict
from knock20 import find_key_in_dictlist
from knock25 import extract_basic_info
from knock26 import remove_emphasis_markup
from knock27 import remove_internal_links

def remove_markup(text: str) -> str:
    """
    MediaWikiマークアップを可能な限り除去する関数

    Args:
        text (str): マークアップ付きテキスト
    Returns:
        str: マークアップ除去後のテキスト
    """
    text = remove_emphasis_markup(text)  # 強調除去
    text = remove_internal_links(text)   # 内部リンク除去
    text = re.sub(r'<.*?>', '', text)  # HTMLタグ除去
    text = re.sub(r'\{\{.*?\}\}', '', text)  # テンプレート除去
    text = re.sub(r'\[.*?\]', '', text)  # 外部リンク除去
    text = re.sub(r'\'+', '', text)  # 残ったシングルクォート除去
    return text.strip()

def fully_clean_basic_info(basic_info: Dict[str, str]) -> Dict[str, str]:
    """
    基礎情報辞書から全てのマークアップを除去する関数
    remove_markup関数を使用する．
    remove_markup関数は，強調マークアップ，内部リンク，HTMLタグ，テンプレート，外部リンクを除去する. (knock26,knock27)

    Args:
        basic_info (Dict[str, str]): 基礎情報辞書（knock25の結果）
    Returns:
        Dict[str, str]: マークアップ除去済みの基礎情報辞書

    """
    cleaned_info = {}
    for field, value in basic_info.items():
        cleaned_info[field] = remove_markup(value)
    return cleaned_info

if __name__ == "__main__":
    filepath = 'json/jawiki-country.json'
    key = 'イギリス'

    articles = find_key_in_dictlist(filepath, key)

    for idx, article in enumerate(articles, start=1):
        print(f"--- 記事 {idx} の基礎情報（完全マークアップ除去後）---")
        # Extract 基礎情報（未加工）
        basic_info = extract_basic_info(article)

        cleaned_info = fully_clean_basic_info(basic_info)

        for field, value in cleaned_info.items():
            print(f"{field}: {value}")
        print("\n")



    """
    (nlp_100knock) nkn4ryu@nkn4ryu-pro chapter03 % python knock28.py
--- 記事 1 の基礎情報（完全マークアップ除去後）---


--- 記事 2 の基礎情報（完全マークアップ除去後）---


--- 記事 3 の基礎情報（完全マークアップ除去後）---
略名: イギリス
日本語国名: グレートブリテン及び北アイルランド連合王国
公式国名: 英語以外での正式国名:
*（スコットランド・ゲール語）
*（ウェールズ語）
*（アイルランド語）
*（コーンウォール語）
*（スコットランド語）
**、（アルスター・スコットランド語）
国旗画像: Flag of the United Kingdom.svg
国章画像: ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章
国章リンク: （イギリスの国章|国章）
標語: （フランス語:Dieu et mon droit|神と我が権利）
国歌: 女王陛下万歳|神よ女王を護り賜え
地図画像: Europe-UK.svg
位置画像: United Kingdom (+overseas territories) in the World (+Antarctica claims).svg
公用語: 英語
首都: ロンドン（事実上）
最大都市: ロンドン
元首等肩書: イギリスの君主|女王
元首等氏名: エリザベス2世
首相等肩書: イギリスの首相|首相
首相等氏名: ボリス・ジョンソン
他元首等肩書1: 貴族院 (イギリス)|貴族院議長
他元首等氏名1: :en:Norman Fowler, Baron Fowler|ノーマン・ファウラー
他元首等肩書2: 庶民院 (イギリス)|庶民院議長
他元首等氏名2: 
他元首等肩書3: 連合王国最高裁判所|最高裁判所長官
他元首等氏名3: :en:Brenda Hale, Baroness Hale of Richmond|ブレンダ・ヘイル
面積順位: 76
面積大きさ: 1 E11
面積値: 244,820
水面積率: 1.3%
人口統計年: 2018
人口順位: 22
人口大きさ: 1 E7
人口値: 6643万5600
人口密度値: 271
GDP統計年元: 2012
GDP値元: 1兆5478億
GDP統計年MER: 2012
GDP順位MER: 6
GDP値MER: 2兆4337億
GDP統計年: 2012
GDP順位: 6
GDP値: 2兆3162億
GDP/人: 36,727
建国形態: 建国
確立形態1: イングランド王国／スコットランド王国（両国とも合同法 (1707年)|1707年合同法まで）
確立年月日1: 927年／843年
確立形態2: グレートブリテン王国成立（1707年合同法）
確立年月日2: 1707年5月1日
確立形態3: グレートブリテン及びアイルランド連合王国成立（合同法 (1800年)|1800年合同法）
確立年月日3: 1801年1月1日
確立形態4: 現在の国号「グレートブリテン及び北アイルランド連合王国」に変更
確立年月日4: 1927年4月12日
通貨: スターリング・ポンド|UKポンド (£)
通貨コード: GBP
時間帯: ±0
夏時間: +1
ISO 3166-1: GB / GBR
ccTLD: .uk / .gb使用は.ukに比べ圧倒的少数。
国際電話番号: 44


(nlp_100knock) nkn4ryu@nkn4ryu-pro chapter03 % 


    """