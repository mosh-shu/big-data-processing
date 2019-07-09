import csv
import sys

path = sys.argv[1]

file = path + "all.csv"
outs = list()

csv_file = open(file, "r", encoding="utf_8")
f = csv.reader(csv_file, delimiter=",", lineterminator="\r\n", quotechar='"',
               skipinitialspace=True)

for row in f:
    if float(row[1]) > 200:
        print(row)
        continue
    if float(row[0]) > 35.7:
        print(row)
        continue
    out = row
    outs.append(out)

with open(file, 'w') as ff:
    writer = csv.writer(ff, lineterminator='\n')  # 改行コード（\n）を指定しておく
    writer.writerows(outs)  # 2次元配列も書き込める
