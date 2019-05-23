#!/usr/bin/env python3.6
import sys
 
args = sys.argv

t, c = sys.stdin.readline().strip().split("\t")
title, count, maxDiff, prev_c = t, int(c), 0, int(c)
for line in sys.stdin:
    t, c = line.strip().split("\t")
    if title != t:
        if count > int(args[1]):
            print(title, "\t", maxDiff);
        title, count, maxDiff, prev_c = t, int(c), 0, int(c)
    else:
        diff = int(c) - prev_c
        if diff > maxDiff:
            maxDiff = diff
        prev_c = int(c)
if count > int(args[1]):
    print(title, "\t", maxDiff);
