track <- read.csv("nagoya/TrackingSpeedData/all.csv", header=F)
png("report/images/allplot_raw.png", width = 700, height = 700)  # 描画デバイスを開く
plot(track[,2], track[,1])
dev.off()

track_d <- read.csv("nagoya/TrackingSpeedData/all_denoise.csv", header=F)
png("report/images/allplot_denoise.png", width = 700, height = 700)  # 描画デバイスを開く
plot(track_d[,2], track_d[,1])
dev.off()

library(ggmap)
library(ggplot2)
register_google(key="*")
map <- get_map(location=c(min(track[,2]), min(track[,1]), max(track[,2]), max(track[,1])),source='google')
ggmap(map)
track[,3] <- as.POSIXct(track[,3], "%Y-%m-%dT%H:%M:%S", tz="Japan")
ggmap(map) + geom_point(data=track, aes(track[,2], track[,1]), color='red')
MissCol <- miss_cat(track, var1 = colnames(track[1]), var2 = colnames(track[2]))

