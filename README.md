# AirTote.Backend

`upload`ディレクトリ内の全てのファイルが自動でデプロイされます。

使用しているサーバは、[LOLIPOP!](https://lolipop.jp/)のハイスピードプランです。
サーバの仕様は[公式ページ](https://lolipop.jp/service/server-spec/)をご確認ください


cronで5分ごとにキャッシュを更新するようにしています。

- Cached METAR: https://d.airtote.jp/GetMetarTaf/metar_jp.csv
- Cached TAF: https://d.airtote.jp/GetMetarTaf/taf_jp.csv

## 設定ファイル

`~/.airtote.backend/config.ini`に配置されることを想定しています

以下にサンプルを示します

```config.ini:ini
[mysql]
db_name = xxx
db_host = xxx.xxx.xxx.xxx
db_user = xxx
db_password = xxx
```
