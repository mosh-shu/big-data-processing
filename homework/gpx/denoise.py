import csv, sys

file = path + "all.csv"
outs = list()

csv_file = open(file, "r", encoding="udf_8")
f = csv.reader(csv_file, delimiter=",",lineterminator="\r\n", quotechar='"', \
                skipinitialspace=True)

for row in f:
    if row[0][2] > 200:
        continue
    out = row
    outs.append(out)

with open(file, 'w') as ff:
    writer = csv.writer(ff, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(outs) # 2次元配列も書き込める