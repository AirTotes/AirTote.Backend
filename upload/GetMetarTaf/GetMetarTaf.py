from mysql.connector import MySQLConnection
import db
from urllib.request import urlopen
from contextlib import closing
import parse_xml_to_csv
from csv import DictWriter
from datetime import datetime

METAR_SOURCE_URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=~jp&hoursBeforeNow=0.4&mostRecentForEachStation=true&fields=station_id,raw_text,observation_time'

COL_STATION_ID = 'station_id'
COL_RAW_TEXT = 'raw_text'
COL_EFFECT_TIME = 'effect_time'
COL_CREATED_AT = 'created_at'

def Q_CREATE_MAIN_TABLE(table_name: str) -> str:
  return f'''CREATE TABLE IF NOT EXISTS {table_name}
  (
    {COL_STATION_ID} VARCHAR(4) NOT NULL,
    {COL_RAW_TEXT} VARCHAR(1024) NOT NULL,
    {COL_EFFECT_TIME} DATETIME NOT NULL,
    {COL_CREATED_AT} DATETIME NOT NULL,
    UNIQUE({COL_STATION_ID}, {COL_RAW_TEXT}, {COL_EFFECT_TIME})
  ) CHARACTER SET ascii COLLATE ascii_general_ci'''

def Q_INSERT_DATA_TO_MAIN_TABLE(table_name: str) -> str:
  return f'''INSERT INTO {table_name}
  ({COL_STATION_ID}, {COL_RAW_TEXT}, {COL_EFFECT_TIME}, {COL_CREATED_AT}) VALUES (%s, %s, %s, CONVERT(%s, DATETIME))
  ON DUPLICATE KEY UPDATE {COL_CREATED_AT} = {COL_CREATED_AT}'''

def Q_SELECT_DATA(table_name: str) -> str:
  return f'''SELECT
  {COL_STATION_ID}, {COL_RAW_TEXT}, {COL_EFFECT_TIME}
  FROM {table_name} INNER JOIN (
      SELECT {COL_STATION_ID} AS sta_id, MAX({COL_CREATED_AT}) AS {COL_CREATED_AT} from {table_name} GROUP BY sta_id
  ) AS A ON {table_name}.{COL_STATION_ID} = A.sta_id AND {table_name}.{COL_CREATED_AT} = A.{COL_CREATED_AT}
  WHERE {COL_STATION_ID} LIKE 'RJ%' OR {COL_STATION_ID} LIKE 'RO%' ORDER BY {COL_STATION_ID} ASC'''

def Q_COUNT_UPDATED_ROWS(table_name: str) -> str:
  return f'SELECT COUNT({COL_STATION_ID}) FROM {table_name} WHERE {COL_CREATED_AT} = CONVERT(%s, DATETIME)'

def update_db_rows(cnx: MySQLConnection, src_url: str, data_name: str, effect_time_elem_name: str) -> int:
  parse_result = parse_xml_to_csv.parse(urlopen(src_url), data_name, effect_time_elem_name)

  CURRENT_TIME = datetime.now()
  TABLE_NAME = data_name.lower()
  with closing(cnx.cursor()) as cursor:
    cursor.execute(Q_CREATE_MAIN_TABLE(TABLE_NAME))

    cursor.executemany(Q_INSERT_DATA_TO_MAIN_TABLE(TABLE_NAME), [(v.station_id, v.raw_text, v.effected_date, CURRENT_TIME) for v in parse_result])
    cnx.commit()

  # tableが更新されていない場合、csvを更新する必要もないので、ここでreturnしてしまう。  
  with closing(cnx.cursor()) as cursor:
    cursor.execute(Q_COUNT_UPDATED_ROWS(TABLE_NAME), (CURRENT_TIME,))

    result = cursor.fetchone()
    return int(result[0])

def write_csv(cnx: MySQLConnection, data_name: str, csv_file_name: str):
  TABLE_NAME = data_name.lower()
  with closing(cnx.cursor(dictionary=True)) as cursor:
    cursor.execute(Q_SELECT_DATA(TABLE_NAME))
    result = cursor.fetchall()
    if len(result) <= 0:
      return

    with open(csv_file_name, 'w') as f:
      writer = DictWriter(f, result[0].keys())
      writer.writeheader()
      writer.writerows(result)


def main(src_url: str, data_name: str, effect_time_elem_name: str, csv_file_name: str):
  try:
    cnx = db.getConnection()

    updated_row_count = update_db_rows(cnx, src_url, data_name, effect_time_elem_name)

    if updated_row_count <= 0:
      return

    write_csv(cnx, data_name, csv_file_name)

  finally:
    cnx.close()

if __name__ == '__main__':
  main(METAR_SOURCE_URL, "METAR", "observation_time", "metar_jp.csv")
