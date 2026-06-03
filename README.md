# karaoke-search

カラオケBanBanの店舗情報を取得し、都道府県・市区町村・設備条件で検索するためのスクリプト群です。

## ファイル説明

### `search.py`

`branches.csv` を読み込み、対話形式で店舗を検索するメインスクリプトです。

都道府県、市区町村、条件を順番に選択すると、該当する店舗名・住所・URLを表示します。条件は以下に対応しています。

- 駐車場有
- Wi-Fi有
- 持ち込み可
- 喫煙所有

都道府県と市区町村の一覧は `dict_pref_city.py` の辞書を参照します。

### `scraping_karaokebanban.py`

カラオケBanBanの店舗一覧ページをスクレイピングし、店舗データを `branches.csv` に書き出すスクリプトです。

取得する主な項目は以下です。

- カラオケチェーン名
- 店舗名
- 店舗ページURL
- 都道府県
- 市区町村
- 住所
- 駐車場の有無
- Wi-Fiの有無
- 持ち込み可否
- 喫煙所の有無

スクレイピングには `requests` と `beautifulsoup4` を使用します。

### `dict_pref_city.py`

都道府県と市区町村の辞書データをまとめたファイルです。

主に以下の辞書を定義しています。

- `dict_pref`: 都道府県ID、都道府県名、表記ゆれ用の別名
- `dict_city`: 市区町村ID、市区町村名、都道府県ID、表記ゆれ用の別名
- `dict_pref_city_id`: 都道府県IDごとの市区町村ID一覧

カラオケBanBanの住所表記に対応するため、千葉県鎌ケ谷市は `鎌ケ谷市` と `鎌ヶ谷市` の2種類の表記を alias に入れています。

### `branches.csv`

検索対象になる店舗データです。

`scraping_karaokebanban.py` を実行すると、このファイルが生成・更新されます。`search.py` はこのCSVを読み込んで検索します。

列の意味は以下です。

- `chain`: カラオケチェーン名
- `branch`: 店舗名
- `url`: 店舗ページURL
- `pref`: 都道府県
- `city`: 市区町村
- `address`: 住所
- `parking`: 駐車場があれば `1`
- `wifi`: Wi-Fiがあれば `1`
- `bringin`: 持ち込み可なら `1`
- `smoking`: 喫煙所があれば `1`

### `test.py`

スクレイピング時にHTML要素や属性の取得方法を確認するための試験用スクリプトです。

現在はカラオケBanBanの埼玉県ページを取得し、最初の店舗情報内にある画像の `alt` 属性を表示します。

## 実行方法

店舗データを更新する場合:

```bash
python scraping_karaokebanban.py
```

店舗を検索する場合:

```bash
python search.py
```

## 注意点

カラオケBanBanのページ側の表示の影響で、佐賀県だけパンくずなどの都道府県表示が `佐賀県` ではなく `佐賀` になっています。おそらくサイト作成者側のミスです。

そのため、`scraping_karaokebanban.py` で `branches.csv` を生成した後、佐賀県の店舗については `pref` を `佐賀県` にし、市区町村も正しく入るように `branches.csv` を手動で修正する必要があります。
