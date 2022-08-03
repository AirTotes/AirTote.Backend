# AirTote.Backend

`upload`ディレクトリ内の全てのファイルが自動でデプロイされます。

使用しているサーバは、[LOLIPOP!](https://lolipop.jp/)のハイスピードプランです。
サーバの仕様は[公式ページ](https://lolipop.jp/service/server-spec/)をご確認ください


cronで5分ごとにキャッシュを更新するようにしています。

- Cached METAR: https://fis-j.technotter.com/GetMetarTaf/metar_jp.csv
- Cached TAF: https://fis-j.technotter.com/GetMetarTaf/taf_jp.csv
