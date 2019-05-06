curl -4 https://dumps.wikimedia.org/other/pageviews/2019/2019-04/ | grep 'href="pageviews' | sed 's/.*href-"//' | sed 's/".*//'

mkdir pv201904
for f in `cat wiki-list.txt`; do
  curl -4 -o pv201904/$f
  https://dumps.wikimedia.org/other/pageviews/2019/2019-04/$f
done

hdfs dfs -put pv201905

haodop jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar -input pv201904 -output pv201904_out -mapper 'wc -l' -reducer cat
# hdfs上のpv_201904 を pv201904_outにreduceし, wc-lをしたものをcatする
