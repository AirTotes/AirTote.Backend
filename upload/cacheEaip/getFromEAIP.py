from dataclasses import dataclass
from sys import argv, stderr
import os
from datetime import datetime
from dateutil import parser
from getFromAISJapan import AISJapan
from typing import Dict, List
from pandas import read_html

@dataclass
class eAIP:
	__date_format = '%Y%m%d'
	__AISJapan: AISJapan
	EffectiveDate: datetime
	PublicationDate: datetime

	def getEffectiveDateStr(self) -> str:
		return self.EffectiveDate.strftime(self.__date_format)
	def getPublicationDateStr(self) -> str:
		return self.PublicationDate.strftime(self.__date_format)

	def get(self, resourceName: str) -> str:
		pubDate = self.getPublicationDateStr()
		effDate = self.getEffectiveDateStr()
		return self.__AISJapan.get(
			f'https://aisjapan.mlit.go.jp/html/AIP/html/{pubDate}/eAIP/{effDate}/{resourceName}'
		)

class eAIPDates:
	__AISJapan: AISJapan
	Dates: Dict[datetime, List[datetime]]
	AIRAC: List[datetime]

	def __init__(self, aisJapan: AISJapan) -> None:
		self.__AISJapan = aisJapan
		self.Dates = {}
		self.AIRAC = []
		dfs = read_html(aisJapan.get('https://aisjapan.mlit.go.jp/html/AIP/html/DomesticAIP.do'))

		if len(dfs) < 1:
			return

		for table in dfs[1:]:
			for i in range(len(table))[1:]:
				row = table.loc[i]

				effectiveDate = parser.parse(row.at[table.columns[1]]).date()
				publicationDate = parser.parse(row.at[table.columns[2]]).date()

				if publicationDate not in self.Dates:
					self.Dates[publicationDate] = []

				if effectiveDate not in self.Dates[publicationDate]:
					self.Dates[publicationDate].append(effectiveDate)
				
				if row.at[table.columns[3]] == 'AIRAC' and effectiveDate not in self.AIRAC:
					self.AIRAC.append(effectiveDate)

	def getLatestCurrent(self) -> eAIP:
		today = datetime.now().date()
		publicationDate = max([v for v in self.Dates.keys() if v <= today])
		effectiveDate = max([v for v in self.Dates[publicationDate] if v <= today])
		return eAIP(self.__AISJapan, effectiveDate, publicationDate)

def dumpToFile(eaip: eAIP, resourceName: str, outDir: str, fileName: str):
	path = os.path.join(outDir, eaip.getPublicationDateStr(), eaip.getEffectiveDateStr(), fileName)
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as f:
		f.write(eaip.get(resourceName))

if __name__ == '__main__':
	if len(argv) < 4:
		print(f'''usage:
\tpython {argv[0]} USER_ID PASSWORD RESOURCE_NAME [CURRENT OUTDIR FILENAME | ALL OUTDIR FILENAME | EFFECTIVE_DATE PUBLICATION_DATE]

\tCURRENT / ALL mode: output file will be ... ./OUTDIR/PublicationDate/EffectiveDate/FILENAME
\t           others : output will be written to stdout
''', file=stderr)
		exit(0)

	aisJapan = AISJapan(argv[1], argv[2])
	eaip: eAIP = None
	if len(argv) > 4:
		if argv[4] == 'CURRENT':
			dumpToFile(eAIPDates(aisJapan).getLatestCurrent(), argv[3], argv[5], argv[6])
		elif argv[4] == 'ALL':
			dates = eAIPDates(aisJapan)
			for pub, effList in dates.Dates.items():
				for eff in effList:
					dumpToFile(eAIP(aisJapan, eff, pub), argv[3], argv[5], argv[6])
		else:
			eaip = eAIP(aisJapan, parser.parse(argv[4]).date(), parser.parse(argv[5]).date())
	else:
		eaip = eAIPDates(aisJapan).getLatestCurrent()

	if eaip is not None:
		print(eaip.get(argv[3]))