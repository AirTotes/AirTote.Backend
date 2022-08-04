from mysql.connector import MySQLConnection
from sys import stdout
import db
from urllib.request import urlopen
from contextlib import closing
import parse_xml_to_csv
from csv import DictWriter
from datetime import datetime

SOURCE_URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=~jp&hoursBeforeNow=0.4&mostRecentForEachStation=true&fields=station_id,raw_text,observation_time'

MAIN_TABLE_NAME = 'metar'
COL_STATION_ID = 'station_id'
COL_RAW_TEXT = 'raw_text'
COL_OBSERVATION_TIME = 'observation_time'
COL_CREATED_AT = 'created_at'

Q_CREATE_MAIN_TABLE = f'''CREATE TABLE IF NOT EXISTS {MAIN_TABLE_NAME}
(
  {COL_STATION_ID} VARCHAR(4) NOT NULL,
  {COL_RAW_TEXT} VARCHAR(1024) NOT NULL,
  {COL_OBSERVATION_TIME} DATETIME NOT NULL,
  {COL_CREATED_AT} DATETIME NOT NULL,
  UNIQUE({COL_STATION_ID}, {COL_RAW_TEXT}, {COL_OBSERVATION_TIME})
) CHARACTER SET ascii COLLATE ascii_general_ci'''

Q_INSERT_DATA_TO_MAIN_TABLE = f'''INSERT INTO {MAIN_TABLE_NAME}
({COL_STATION_ID}, {COL_RAW_TEXT}, {COL_OBSERVATION_TIME}, {COL_CREATED_AT}) VALUES (%s, %s, %s, CONVERT(%s, DATETIME))
ON DUPLICATE KEY UPDATE {COL_CREATED_AT} = {COL_CREATED_AT}'''

Q_SELECT_DATA = f'''SELECT
{COL_STATION_ID}, {COL_RAW_TEXT}, {COL_OBSERVATION_TIME}
FROM {MAIN_TABLE_NAME} INNER JOIN (
    SELECT {COL_STATION_ID} AS sta_id, MAX({COL_CREATED_AT}) AS {COL_CREATED_AT} from {MAIN_TABLE_NAME} GROUP BY sta_id
) AS A ON {MAIN_TABLE_NAME}.{COL_STATION_ID} = A.sta_id AND {MAIN_TABLE_NAME}.{COL_CREATED_AT} = A.{COL_CREATED_AT}
WHERE {COL_STATION_ID} LIKE 'RJ%' OR {COL_STATION_ID} LIKE 'RO%' ORDER BY {COL_STATION_ID} ASC
'''

Q_COUNT_UPDATED_ROWS = f'SELECT COUNT({COL_STATION_ID}) FROM {MAIN_TABLE_NAME} WHERE {COL_CREATED_AT} = CONVERT(%s, DATETIME)'

def update_db_rows(cnx: MySQLConnection) -> int:
  parse_result = parse_xml_to_csv.parse(urlopen(SOURCE_URL), "METAR", "observation_time")

  CURRENT_TIME = datetime.now()
  with closing(cnx.cursor()) as cursor:
    cursor.execute(Q_CREATE_MAIN_TABLE)

    cursor.executemany(Q_INSERT_DATA_TO_MAIN_TABLE, [(v.station_id, v.raw_text, v.effected_date, CURRENT_TIME) for v in parse_result])
    cnx.commit()

  # tableが更新されていない場合、csvを更新する必要もないので、ここでreturnしてしまう。  
  with closing(cnx.cursor()) as cursor:
    cursor.execute(Q_COUNT_UPDATED_ROWS, (CURRENT_TIME,))

    result = cursor.fetchone()
    return int(result[0])

def write_csv(cnx: MySQLConnection):
  with closing(cnx.cursor(dictionary=True)) as cursor:
    cursor.execute(Q_SELECT_DATA)
    result = cursor.fetchall()
    if len(result) <= 0:
      return

    writer = DictWriter(stdout, result[0].keys())
    writer.writeheader()
    writer.writerows(result)


def main():
  try:
    cnx = db.getConnection()

    updated_row_count = update_db_rows(cnx)

    print(updated_row_count)
    if updated_row_count <= 0:
      return

    write_csv(cnx)

  finally:
    cnx.close()

if __name__ == '__main__':
  main()
