import json

def get_dictlist_from_json(file_path):
    out = []
    
    with open(file_path, 'r') as file:
        for item in file:
            json_dict= json.loads(item)
            out.append(json_dict)
            
    return out

    # loads は文字列を引数にとって辞書型で返す
    # https://zenn.dev/milkystack/articles/a5b94da6ab6542
    

def find_key_in_dictlist(path:str, key)->list[str]:
    out = []
    dictlist = get_dictlist_from_json(path)
    for item in dictlist:
        if key in item['title']:
            out.append(item['text'])
    return out

if __name__== "__main__":

    key = 'イギリス'
    filepath = 'json/jawiki-country.json'
    
    out = find_key_in_dictlist(filepath,key)
    
    print(len(out))
    for item in out:
        print(item)
    
    
    
    