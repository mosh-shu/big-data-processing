# SPD.csvを時刻順に処理する

path=$1
files=`find $path -maxdepth 1 -type f -name SPD*.csv`

for file in $files;
do
    newfile="${file:0:-4}_sorted.csv"
    echo $newfile
    sort -t , -k 1 $file > $newfile
    # ここから実行処理を記述
done
