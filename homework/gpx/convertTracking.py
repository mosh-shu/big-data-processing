import csv
import sys
import glob


def getDegree(s):
    v0_bin = format(int(s[0:2], 16), 'b').zfill(8)
    v1_bin = format(int(s[2:4], 16), 'b').zfill(8)
    v2_bin = format(int(s[4:6], 16), 'b').zfill(8)
    v3_bin = format(int(s[6:8], 16), 'b').zfill(8)

    bin_bit = v0_bin[1:] + v1_bin[1:] + v2_bin[1:] + v3_bin[1:]

    hex_int = ''
    for i in range(7):
        hex_int += str(format(int(bin_bit[i*4:i*4+4], 2), 'x'))

    dec_int = int(hex_int, 16)

    deg = dec_int / 60000.0

    return str(deg)


def getISO8601(s):
    ye = int(s[0:2]) + 2000
    mo = int(s[2:4])
    da = int(s[4:6])
    h = int(s[8:10])
    m = int(s[10:12])
    s = int(s[12:14])
    return ("{:04}-{:02}-{:02}T{:02}:{:02}:{:02}+09:00".format(ye, mo, da, h, m, s))


path = sys.argv[1]

files = glob.glob(path + "GPS*.csv")
outs = [["lon", "lat", "time", "orientation", "tariff", "high"]]

for file in files:
    csv_file = open(file, "r", encoding="shift_jis")
    f = csv.reader(csv_file, delimiter=",", lineterminator="\r\n",
                   quotechar='"', skipinitialspace=True)

    print(file)

    for row in f:
        if row == []:
            continue
        lon = getDegree(row[0][0:8])
        lat = getDegree(row[0][8:16])
        time = getISO8601(row[0][16:30])
        orientation = str(int(row[0][30:34], 16))
        tariff = row[1]
        high = row[2][0:2]
        out = [lon, lat, time, orientation, tariff, high]
        outs.append(out)

    outfile = file[:-4] + "_conv.csv"

    with open(outfile, 'w', encoding="utf_8") as ff:
        writer = csv.writer(ff, lineterminator='\n')  # 改行コード（\n）を指定しておく
        writer.writerows(outs)  # 2次元配列も書き込める
