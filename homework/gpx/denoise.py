import csv
import sys

path = sys.argv[1]

file = path + "all.csv"
newfile = path + "all_denoise.csv"
outs = list()

csv_file = open(file, "r", encoding="utf_8")
f = csv.reader(csv_file, delimiter=",", lineterminator="\r\n", quotechar='"',
               skipinitialspace=True)

for row in f:
    if not 136.4 < float(row[1]) < 137.5:
        continue
    if not 34.6 < float(row[0]) < 35.6:
        continue
    out = row
    outs.append(out)

with open(newfile, 'w') as ff:
    writer = csv.writer(ff, lineterminator='\n')  # 改行コード（\n）を指定しておく
    writer.writerows(outs)  # 2次元配列も書き込める
