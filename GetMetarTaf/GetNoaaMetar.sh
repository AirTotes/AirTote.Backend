#!/bin/bash

DB_FILE_NAME='metar_taf.db'
IMPORT_CACHE_SQL_FILE_NAME='import_noaa_metar.sql'
SHOW_RECORDS_CSV_SQL_FILE_NAME='show_jp_metar.sql'
SOURCE_URL='https://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv'
SOURCE_FILE_NAME='metars.cache.csv'
LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME='metar_noaa.date.log'
OUTPUT_CSV_FILE_NAME='metar_jp.csv'
DATE_CMD='date'
ERR_HEAD_LOG_DIR='metar_cache_err_log'

cd `dirname $0`

# サーバ上のキャッシュの最終更新時刻をチェックする
SOURCE_LAST_MODIFIED=`curl --head "$SOURCE_URL" 2> /dev/null | grep -i "last-modified" | sed -e "s/last-modified: //i"`

if [ ! -d $ERR_HEAD_LOG_DIR ]; then
  mkdir $ERR_HEAD_LOG_DIR
fi

# 何らかの原因でデータ取得に失敗している
if [ "$SOURCE_LAST_MODIFIED" == "" ]; then
  curl --head "$SOURCE_URL" > "$ERR_HEAD_LOG_DIR/`date`.log"
  exit 1
fi

if [ `uname` = 'Darwin' ]; then
  DATE_CMD='gdate'
fi

SOURCE_LAST_MODIFIED=`TZ=UTC $DATE_CMD "+%F %T" -d "$SOURCE_LAST_MODIFIED"`

# 最終更新が手元のキャッシュと同一であれば、それを採用しない。
if [ -f "$LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME" ] && [ "`cat "$LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME"`" == "$SOURCE_LAST_MODIFIED" ]; then
  exit 0;
fi

# 最後の改行なしで、リモートのファイル編集時刻をキャッシュする
echo -n "$SOURCE_LAST_MODIFIED" > $LOCAL_CACHE_MODIFIED_DATE_RECORD_FILE_NAME

# キャッシュをサーバから取得
# 先頭の不要な行を削除する
curl "$SOURCE_URL" 2> /dev/null | sed '1,6d' > $SOURCE_FILE_NAME

# NOAAのキャッシュから、手元のキャッシュを更新するコード
sqlite3 $DB_FILE_NAME < $IMPORT_CACHE_SQL_FILE_NAME

# 現在のMETARをcsvに書き出す
sqlite3 $DB_FILE_NAME < $SHOW_RECORDS_CSV_SQL_FILE_NAME > $OUTPUT_CSV_FILE_NAME

# NOAAから取得したMETARのcsvを削除する
rm -f "$SOURCE_FILE_NAME"
