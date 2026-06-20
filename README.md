# karaoke-search

カラオケチェーンの店舗情報をスクレイピングで取得し、都道府県・市区町村・条件でチェーン横断的に検索するためのプロジェクトリポジトリ。

## セットアップ

プロジェクトディレクトリに移動し、仮想環境を有効化する。

```bash
cd ~/Documents/projects/karaoke-search
source .venv/bin/activate
```

プロジェクトを終了する際には、ホームディレクトリに移動し、仮想環境を無効化する。

```bash
cd ~
deactivate
```

## スクレイピング

カラオケBanBanの店舗情報を取得し、`karaoke_search.db` を更新する。

```bash
python3 scripts/banban/scraping_banban.py
```

スクレイピングをやり直す場合は、`db/karaoke_search.db` をコピーして、ルート直下にペーストする。

## 検索

`karaoke_search.db` を使って、都道府県・市区町村・条件で店舗を検索する。

```bash
python3 scripts/search.py
```

実行後は、画面の案内に沿って以下を入力する。

1. 都道府県の番号
2. 市区町村の番号
3. 検索条件

検索条件は以下の番号で指定する。

- `0`: 条件なし
- `1`: 駐車場有
- `2`: Wi-Fi有
- `3`: 持ち込み可
- `4`: 喫煙所有

複数条件で検索したい場合は、番号を続けて入力する。たとえば、駐車場有かつWi-Fi有で検索する場合は `12` と入力する。

該当する店舗がある場合は、店舗名・住所・店舗ページURLが表示され、該当店舗がない場合は、`該当する店舗はありません。` と表示される。

## その他

- `db/karaoke_search.db`において、北海道内に同名の `泊村` が `city_code`: `66` および `city_code`: `181` として存在しているが、前者は古宇郡、後者は国後郡に属する別の村である。

- カラオケBanBanの都道府県の店舗ページで、千葉県（`https://karaoke-shin.jp/shop-area/12.html`）鎌ケ谷市の店舗について、dbの表記`鎌ケ谷市`とBanBanの表記`鎌ヶ谷市`の表記揺れがある。
そのため、`scraping_banban.py` で `karaoke_search.db` を更新した後、千葉県鎌ケ谷市の店舗については手動で修正する必要がある。

- カラオケBanBanの都道府県の店舗ページで、佐賀県（`https://karaoke-shin.jp/shop-area/41.html`）だけパンくずなどの都道府県表示が `佐賀県` ではなく `佐賀` になっている（おそらくサイト作成者側のミス）。
そのため、`scraping_banban.py` で `karaoke_search.db` を更新した後、佐賀県の店舗については手動で修正する必要がある。
