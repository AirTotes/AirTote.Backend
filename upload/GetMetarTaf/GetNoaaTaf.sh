#!/bin/bash

DB_FILE_NAME='metar_taf.db'
IMPORT_CACHE_SQL_FILE_NAME='sql/import_noaa_taf.sql'
SHOW_RECORDS_CSV_SQL_FILE_NAME='sql/show_jp_taf.sql'
SOURCE_URL='https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=~jp&hoursBeforeNow=0.4&timeType=issue&mostRecentForEachStation=true&fields=station_id,raw_text,issue_time'
SOURCE_FILE_NAME='tafs.cache.csv'
XML_TO_CSV_PY_FILE_NAME='parse_xml_to_csv.py'
OUTPUT_CSV_FILE_NAME='taf_jp.csv'

cd `dirname $0`

# データをサーバから取得
# XMLからcsvに変換しておく
# NOAAのキャッシュから、手元のキャッシュを更新するコード
curl "$SOURCE_URL" 2> /dev/null | python $XML_TO_CSV_PY_FILE_NAME "TAF" "issue_time" > $SOURCE_FILE_NAME

sqlite3 $DB_FILE_NAME < $IMPORT_CACHE_SQL_FILE_NAME

# 現在のTAFをcsvに書き出す
sqlite3 $DB_FILE_NAME < $SHOW_RECORDS_CSV_SQL_FILE_NAME > $SOURCE_FILE_NAME

if [ -f $OUTPUT_CSV_FILE_NAME ] && [ `diff $SOURCE_FILE_NAME $OUTPUT_CSV_FILE_NAME | wc -l` == "0" ]; then
  # NOAAから取得したTAFのcsvを削除する
  rm -f "$SOURCE_FILE_NAME"
else
  mv $SOURCE_FILE_NAME $OUTPUT_CSV_FILE_NAME
fi
