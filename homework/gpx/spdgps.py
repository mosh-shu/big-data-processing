import csv
import sys
import glob
import datetime

# functions


def time_spd2gps(tstr):
    ye = tstr[0:4]
    mo = tstr[5:7]
    da = tstr[8:10]
    h = tstr[11:13]
    m = tstr[14:16]
    s = tstr[17:19]

    return ("{}-{}-{}T{}:{}:{}+09:00".format(ye, mo, da, h, m, s))


def sameride(tstr1, tstr2):
    t1 = datetime.datetime(year=int(tstr1[0:4]), month=int(tstr1[5:7]), day=int(tstr1[8:10]),
                           hour=int(tstr1[11:13]), minute=int(tstr1[14:16]), second=int(tstr1[17:19]))
    t2 = datetime.datetime(year=int(tstr2[0:4]), month=int(tstr2[5:7]), day=int(tstr2[8:10]),
                           hour=int(tstr2[11:13]), minute=int(tstr2[14:16]), second=int(tstr2[17:19]))
    if s2 -


# init
path_gps = sys.argv[1]  # nagoya/TrackingData/
path_spd = sys.argv[2]  # nagoya/SpeedData/
path_dst = sys.argv[3]  # nagoya/TrackingSpeedData/

files_gps = glob.glob(path_gps + "GPS102_conv.csv")
files_spd = glob.glob(path_spd + "SPD102_sorted.csv")

# main
for file_spd in files_spd:

    idstr = file_spd[-14:-11]
    file_gps = path_gps + "GPS" + idstr + "_conv.csv"
    if file_gps not in files_gps:
        continue

    print("reading {}...".format(file_spd))

    # spd の読み込み
    # 2013/08/01 08:53:01.0,0,0
    data_spd = []
    times_spd = []
    with open(file_spd, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row == []:
                continue
            if row[0][-1] == '5':
                continue

            row[0] = time_spd2gps(row[0])
            data_spd.append(row)
            times_spd.append(row[0])

    print("reading {}...".format(file_gps))

    # gps の読み込み
    # ヘッダあり, 35.130516666666665,136.98396666666667,2013-07-31T20:32:15+09:00,2661,00,00
    data_gps = []
    times_gps = []
    with open(file_gps, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            #  もしgpsの時刻がspdになければ, 行を削除
            # そうでなければ二次元配列data_gpsに格納
            # 時刻をtime_gpsに格
            if row == []:
                continue
            time_gps = row[2]
            if time_gps not in times_spd:
                continue

            times_gps.append(time_gps)
            data_gps.append(row)

    print("data_spd\n", data_spd[:10])
    print("data_gps\n", data_gps[:10])

    for idx_spd, datum_spd in enumerate(data_spd):
        if datum_spd[0] != times_gps[0]
        # if (datum_spd.time not in time_gps) and sameride(datum_spd.time, datum_spd[n+1].time)
        # もしspdの時刻がgpsに含まれておらず (time_gpsの隙間)
        # かつ次のspdの時刻が離れていないなら (時刻がジャンプ)
        # data_spdをspd_nongps取っておく
        # else
        # spd_nongps[0] ~ data_spd.timeでGPS位置を補間し, 時間を合わせる処理
        #
