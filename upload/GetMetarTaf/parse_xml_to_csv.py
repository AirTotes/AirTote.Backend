import csv
from sys import stdin, stdout, argv
from xml.etree import ElementTree

METARs = ElementTree.parse(stdin).getroot().find("data").findall(argv[1])

csv.writer(stdout).writerows([
  [
    metar.find("station_id").text,
    metar.find("raw_text").text,
    metar.find(argv[2]).text
  ] for metar in METARs])
