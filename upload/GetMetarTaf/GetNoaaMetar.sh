#!/bin/bash

DB_FILE_NAME='metar_taf.db'
IMPORT_CACHE_SQL_FILE_NAME='sql/import_noaa_metar.sql'
SHOW_RECORDS_CSV_SQL_FILE_NAME='sql/show_jp_metar.sql'
SOURCE_URL='https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=~jp&hoursBeforeNow=0.4&mostRecentForEachStation=true&fields=station_id,raw_text,observation_time'
SOURCE_FILE_NAME='metars.cache.csv'
XML_TO_CSV_PY_FILE_NAME='parse_xml_to_csv.py'
OUTPUT_CSV_FILE_NAME='metar_jp.csv'

cd `dirname $0`

# データをサーバから取得
# XMLからcsvに変換しておく
# NOAAのキャッシュから、手元のキャッシュを更新するコード
curl "$SOURCE_URL" 2> /dev/null | python $XML_TO_CSV_PY_FILE_NAME "METAR" "observation_time" > $SOURCE_FILE_NAME

sqlite3 $DB_FILE_NAME < $IMPORT_CACHE_SQL_FILE_NAME

# 現在のMETARをcsvに書き出す
sqlite3 $DB_FILE_NAME < $SHOW_RECORDS_CSV_SQL_FILE_NAME > $SOURCE_FILE_NAME

if [ `diff $SOURCE_FILE_NAME $OUTPUT_CSV_FILE_NAME | wc -l` == "0" ]; then
  # NOAAから取得したMETARのcsvを削除する
  rm -f "$SOURCE_FILE_NAME"
else
  mv $SOURCE_FILE_NAME $OUTPUT_CSV_FILE_NAME
fi
