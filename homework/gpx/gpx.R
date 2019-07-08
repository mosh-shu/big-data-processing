# After python convertTracking.py

track <- read.csv("nagoya/TrackingData/all/.csv", header=F)
plot(track[,2], track[,1])