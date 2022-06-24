import csv
import sys

reader = csv.reader(sys.stdin)

csv.writer(sys.stdout).writerows([row[0:3] for row in reader])
