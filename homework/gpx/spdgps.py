import csv, sys, glob, datetime, pprint

## functions

def time_spd2gps(tstr: str) -> str:
    '''
    SPDデータの時刻を, GPSデータの表記に合わせる. 
    Input: 
        tstr: SPDデータの時刻. str型. 
    Output:
        GPSデータ表記の時刻. str型. 
    '''
    ye = tstr[0:4]
    mo = tstr[5:7]
    da = tstr[8:10]
    h = tstr[11:13]
    m = tstr[14:16]
    s = tstr[17:19]

    return ("{}-{}-{}T{}:{}:{}+09:00".format(ye, mo, da, h, m, s))

def sameride(tstr1: str, tstr2: str) -> bool:
    '''
    2つ時刻データ (tstr1, tstr2) が1秒より離れていないか確かめる (データの切れ目をdetectする).
    Input:
        tstr1: 1つ目の時刻データ. str型.
        tstr2: 2つ目の時刻データ. str型.
    Output:
        Bool型. tstr1とtstr2が1秒より離れていなければTrue.それ以外はFalse.
    '''
    t1 = datetime.datetime(year=int(tstr1[0:4]), month=int(tstr1[5:7]), day=int(tstr1[8:10]),
                           hour=int(tstr1[11:13]), minute=int(tstr1[14:16]), second=int(tstr1[17:19]))
    t2 = datetime.datetime(year=int(tstr2[0:4]), month=int(tstr2[5:7]), day=int(tstr2[8:10]),
                           hour=int(tstr2[11:13]), minute=int(tstr2[14:16]), second=int(tstr2[17:19]))
    diff = t2 - t1
    return diff.total_seconds() < 2

## init
path_gps = sys.argv[1]  # nagoya/TrackingData/
path_spd = sys.argv[2]  # nagoya/SpeedData/
path_dst = sys.argv[3]  # nagoya/TrackingSpeedData/

files_gps = glob.glob(path_gps + "GPS*_conv.csv")
files_spd = glob.glob(path_spd + "SPD*_sorted.csv")

## main
for file_spd in files_spd:

    idstr = file_spd[-14:-11]
    file_gps = path_gps + "GPS" + idstr + "_conv.csv"
    file_dst = path_dst + "GPSSPD" + idstr + ".csv"

    if file_gps not in files_gps:
        continue

    print("reading {}...".format(file_spd))

    # spd の読み込み
    # 2013/08/01 08:53:01.0,0,0
    data_spd = []
    times_spd = []
    with open(file_spd, 'r') as f:
        reader = csv.reader(f)
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
    last_row = []
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
            if row==last_row:
                # print(row)
                continue
            times_gps.append(time_gps)
            data_gps.append(row)
            last_row = row

    # print("data_spd")
    # pprint.pprint(data_spd[:10], width=50)
    # print("data_gps")
    # pprint.pprint(data_gps[:10], width=50)

    data_spd_btw = []           # GPS時刻の間にあるSPDデータ
    spd_vel = []                # SPD時刻で補間する時間窓内の速度
    gps_t1 = []                 # SPD時刻で補間されるGPS時刻の開始地点
    gps_t2 = []                 # SPD時刻で補間されるGPS時刻の終了地点
    idx_gps = 0                 # 読んでいるGPSの行を知るためのカウンター
    gps_ndata = len(data_gps)   # GPSデータの総数
    spd_ndata = len(data_spd)   # SPDデータの総数
    data_dst = []               # file_dstに保存する2次元配列
    samerideFlag = True

    print("interpolating gps with spd...")

    for idx_spd, datum_spd in enumerate(data_spd):

        # データが最後に到達したら処理を終える
        if idx_gps == gps_ndata-1 or idx_spd == spd_ndata-1:
            print("\ngps_ndata: {}\nidx_gps: {}\nspd_ndata: {}\nidx_spd: {}"\
                    .format(gps_ndata, idx_gps, spd_ndata, idx_spd))
            break

        # if idx_spd%100000 == 0: print("\nidx_spd: ",str(idx_spd))

        # GPS時刻==SPD時刻まで, (間の) SPD時刻をストックしておく
        time_spd = datum_spd[0]
        time_spd_nxt = data_spd[idx_spd+1][0]
        time_gps = data_gps[idx_gps][2]

        if time_spd != time_gps and sameride(time_spd, time_spd_nxt):
            # print("hi, time_spd{}, time_gps{}".format(time_spd, time_gps))
            data_spd_btw.append(datum_spd)
            continue

        # データの切れ目は切り捨てる
        # 終末の切れ端
        if not sameride(time_spd, time_spd_nxt):
            print("not sameride, idx is {}, data is {}".format(idx_spd, datum_spd))
            # print("previous time_gps: {}\ntime_gps: {}\nnext time_gps: {}\ntime_spd: {}\n".\
                    # format(data_gps[idx_gps-1][2], time_gps, data_gps[idx_gps+1][2], time_spd))            
            data_spd_btw = []
            samerideFlag = False
            continue
        # 始点の切れ端
        if time_gps==time_spd and not samerideFlag:
            print("not samerideFlag, idx is {}, data is {}\n".format(idx_spd, datum_spd))
            # print("time_gps: {}\nnext time_gps: {}\ntime_spd: {}\n\n".format(time_gps, data_gps[idx_gps+1][2], time_spd))
            data_spd_btw = []
            idx_gps += 1
            samerideFlag = True
            continue

        # 最初のGPS時刻は切り捨てる
        if idx_gps == 0:
            data_spd_btw = []
            idx_gps += 1
            continue

        # 補間処理
        # 終点のspdも追加する
        data_spd_btw.append(datum_spd)

        gps_t1 = data_gps[idx_gps-1]
        gps_t2 = data_gps[idx_gps]
        vels_spd_btw = [int(datum_spd_btw[1]) for datum_spd_btw in data_spd_btw]

        vel_total = sum([int(vel_spd_btw) for vel_spd_btw in vels_spd_btw]) + 1 # to avoid div0
        lon_t1 = float(gps_t1[0])
        lon_t2 = float(gps_t2[0])
        lat_t1 = float(gps_t1[1])
        lat_t2 = float(gps_t2[1])
        lon_diff = lon_t2-lon_t1
        lat_diff = lat_t2-lat_t1

        # velによってlon,latを補間する
        # lon,lat,time,tariff,vel
        for datum_spd_btw in data_spd_btw:
            t = datum_spd_btw[0]
            vel = int(datum_spd_btw[1])
            lon = lon_t1 + lon_diff * vel/vel_total
            lat = lat_t1 + lat_diff * vel/vel_total
            tariff = gps_t1[4]
            datum_dst = [str(lon), str(lat), t, tariff, str(vel)]
            data_dst.append(datum_dst)

        data_spd_btw = []
        idx_gps += 1
    
    # ファイルに書き込み
    with open(file_dst, 'w', encoding="utf_8") as ff:
        writer = csv.writer(ff, lineterminator='\n')  # 改行コード（\n）を指定しておく
        writer.writerows(data_dst)  # 2次元配列も書き込める