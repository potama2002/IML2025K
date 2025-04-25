

## knock 20

## knock 21

## knock 22

## knock 23

## knock 24

## knock 25

## knock 26

## knock 27


## knock 28




## knock 29

```json
response = requests.get(endpoint, params=params).json()
```

は，以下の2ステップを一行で書いたもの．
```

response = requests.get(endpoint, params=params)  # 1. GET リクエストを送信 → Response オブジェクトを取得
data = response.json()                             # 2. JSON をパース → Python の dict/list に変換

```


以下は``responce``を出力したもの．送信したHTTPリクエストに対する応答．

``` json

{
  "continue": {
    "iistart": "2023-05-07T10:52:57Z",
    "continue": "||"
  },
  "query": {
    "pages": {
      "127049491": {
        "pageid": 127049491, // page ID
        "ns": 6,
        "title": "File:Flag of the United Kingdom.svg",
        "imagerepository": "local",
        "imageinfo": [
          {
            "url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg",
            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Flag_of_the_United_Kingdom_(3-5).svg",
            "descriptionshorturl": "https://commons.wikimedia.org/w/index.php?curid=895166"
          }
        ]
      }
    }
  }
}


```


