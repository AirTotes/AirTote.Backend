from sys import argv
from datetime import datetime

import getFromAISJapan
import getFromEAIP


def main(USER_ID: str, PASSWORD: str):
  # AIS Japanにサインイン
  aisJapan: getFromAISJapan.AISJapan = getFromAISJapan.AISJapan(USER_ID, PASSWORD)

  # eAIPの対象となる日付を取得する
  eaipDates: getFromEAIP.eAIPDates = getFromEAIP.eAIPDates(aisJapan)

  # 最新のeAIPを取得するインスタンスを取得する
  # eAIP_LatestCurrent: getFromEAIP.eAIP = eaipDates.getLatestCurrent()

  UTCtime = datetime.utcnow().isoformat(timespec ='seconds')
  with open("dates.csv", mode = 'w') as c:
    for publicationDate, effectiveDateList in eaipDates.Dates.items():
      for effectiveDate in effectiveDateList:
        c.write(f"{publicationDate},{effectiveDate},{effectiveDate in eaipDates.AIRAC},{UTCtime}\n")

if __name__ == '__main__':
  # USER_IDとPASSWORDを設定する
  # 例: python3 tmp.py USER_ID PASSWORD
  main(argv[1], argv[2])
