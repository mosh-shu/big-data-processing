curl http://www.data.jma.go.jp/svd/eqev/data/daily_map/20160414.html | nkf -w | grep -e '^2016' -e '^年' | less
