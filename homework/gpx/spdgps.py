import csv, sys, glob, datetime, pprint

# functions


def time_spd2gps(tstr: str) -> str:
    ye = tstr[0:4]
    mo = tstr[5:7]
    da = tstr[8:10]
    h = tstr[11:13]
    m = tstr[14:16]
    s = tstr[17:19]

    return ("{}-{}-{}T{}:{}:{}+09:00".format(ye, mo, da, h, m, s))


def sameride(tstr1: str, tstr2: str) -> bool:
    t1 = datetime.datetime(year=int(tstr1[0:4]), month=int(tstr1[5:7]), day=int(tstr1[8:10]),
                           hour=int(tstr1[11:13]), minute=int(tstr1[14:16]), second=int(tstr1[17:19]))
    t2 = datetime.datetime(year=int(tstr2[0:4]), month=int(tstr2[5:7]), day=int(tstr2[8:10]),
                           hour=int(tstr2[11:13]), minute=int(tstr2[14:16]), second=int(tstr2[17:19]))
    diff = t2 - t1
    return diff.total_seconds() < 2


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
            if row[0][-1] == '5': # ダウンサンプリング
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
            # 時刻をtime_gpsに格納
            if row == []:
                continue

            time_gps = row[2]
            if not time_gps in times_spd:
                continue
            times_gps.append(time_gps)
            data_gps.append(row)

    print("data_spd")
    pprint.pprint(data_spd[:10], width=50)
    print("data_gps")
    pprint.pprint(data_gps[:10], width=50)

    data_spd_btw = []  # GPS時刻の間にあるSPDデータ
    spd_vel = [] # SPD時刻で補間する時間窓内の速度
    gps_t1 = [] # SPD時刻で補間されるGPS時刻の開始地点
    gps_t2 = [] # SPD時刻で補間されるGPS時刻の終了地点
    gps_cnt = 0
    gps_ndata = len(data_gps)

    print("interpolating gps with spd...")

    for idx_spd, datum_spd in enumerate(data_spd[:200]):

        # GPS時刻==SPD時刻まで, (間の) SPD時刻をストックしておく
        time_spd = datum_spd[0]
        time_spd_nxt = data_spd[idx_spd+1][0]
        time_gps = times_gps[0]
        if time_spd != time_gps and sameride(time_spd, time_spd_nxt):
            print("hi, time_spd{}, time_gps{}".format(time_spd, time_gps))
            data_spd_btw.append(datum_spd)
            continue

        # 最初のGPS時刻と最後のGPS時刻は切り捨てる (間が存在しない)
        if gps_cnt == 0:
            gps_t2 = data_gps[gps_cnt]
            data_spd_btw = []
            times_gps = times_gps[1:]
            gps_cnt += 1
            continue
        if gps_cnt == gps_ndata-1:
            break

        gps_t1 = gps_t2
        gps_t2 = data_gps[gps_cnt]
        vels_spd_btw = [int(datum_spd_btw[1]) for datum_spd_btw in data_spd_btw]

        print("gps_t1: ")
        pprint.pprint(gps_t1, width=50)
        print("gps_t2: ")
        pprint.pprint(gps_t2, width=50)
        print(vels_spd_btw)
        print("gps_cnt", gps_cnt)

        data_spd_btw = []
        times_gps = times_gps[1:]
        gps_cnt += 1
            # times_gps[] は一時変数的な扱い, 使ったらpopしていく
            # if (datum_spd.time not in time_gps) and sameride(datum_spd.time, datum_spd[n+1].time)
            # もしspdの時刻がgpsに含まれておらず (time_gpsの隙間)
            # かつ次のspdの時刻が離れていないなら (時刻がジャンプしていないなら)
            # data_spdをspd_nongps取っておく
            # else
            # spd_nongps[0] ~ data_spd.timeでGPS位置を補間し, 時間を合わせる処理
            # times_gps[0] = 0
