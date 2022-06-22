#!/bin/bash

DB_FILE_NAME='metar_taf.db'
IMPORT_NOAA_METAR_CACHE_SQL_FILE_NAME='import_noaa_metar.sql'
SHOW_JP_METAR_SQL_FILE_NAME='show_jp_metar.sql'
NOAA_METAR_CACHE_URL='https://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv'
NOAA_METAR_CACHE_FILE_NAME='metars.cache.csv'
LOG_FILE_PATH='metar_taf.log'
LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME='metar_noaa.date.log'
JP_METAR_CSV='metar_jp.csv'
DATE_CMD='date'

cd `dirname $0`

# サーバ上のキャッシュの最終更新時刻をチェックする
NOAA_CACHE_LAST_MODIFIED=`curl --head "$NOAA_METAR_CACHE_URL" 2> /dev/null | grep "last-modified" | sed -e "s/last-modified: //"`

# 何らかの原因でデータ取得に失敗している
if [ "$NOAA_CACHE_LAST_MODIFIED" == "" ]; then
  echo `date` "[ERROR]" ": Cannot load METAR cache from NOAA server" >> LOG_FILE_PATH
  exit 1
fi

if [ `uname` = 'Darwin' ]; then
  DATE_CMD='gdate'
fi

NOAA_CACHE_LAST_MODIFIED=`TZ=UTC $DATE_CMD "+%F %T" -d "$NOAA_CACHE_LAST_MODIFIED"`

# 最終更新が手元のキャッシュと同一であれば、それを採用しない。
if [ -f "$LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME" ] && [ "`cat "$LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME"`" == "$NOAA_CACHE_LAST_MODIFIED" ]; then
  exit 0;
fi

# 最後の改行なしで、リモートのファイル編集時刻をキャッシュする
echo -n "$NOAA_CACHE_LAST_MODIFIED" > $LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME

# キャッシュをサーバから取得
curl -O "$NOAA_METAR_CACHE_URL" 2> /dev/null

# 先頭の不要な行を削除する
sed '1,6d' "$NOAA_METAR_CACHE_FILE_NAME" > $NOAA_METAR_CACHE_FILE_NAME

# NOAAのキャッシュから、手元のキャッシュを更新するコード
sqlite3 $DB_FILE_NAME < $IMPORT_NOAA_METAR_CACHE_SQL_FILE_NAME

# 現在のMETARをcsvに書き出す
sqlite3 $DB_FILE_NAME < $SHOW_JP_METAR_SQL_FILE_NAME > $JP_METAR_CSV

# NOAAから取得したMETARのcsvを削除する
rm -f "$NOAA_METAR_CACHE_FILE_NAME"
