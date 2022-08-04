import csv
from dataclasses import dataclass
from sys import stdin, stdout, argv
from typing import TextIO
from xml.etree import ElementTree

@dataclass
class csv_columns:
  station_id: str
  raw_text: str
  effected_date: str

  def toArr(self) -> list:
    return [self.station_id, self.raw_text, self.effected_date]

def parse(src: TextIO, target_elem_name: str, effected_date_elem_name: str) -> list[csv_columns]:
  METARs = ElementTree.parse(src).getroot().find("data").findall(target_elem_name)

  return [
    csv_columns(
      metar.find("station_id").text,
      metar.find("raw_text").text,
      metar.find(effected_date_elem_name).text
    ) for metar in METARs]

if __name__ == '__main__':
  csv.writer(stdout).writerows(
    [row.toArr() for row in parse(stdin, argv[1], argv[2])]
  )
