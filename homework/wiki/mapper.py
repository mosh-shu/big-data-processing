#!/usr/bin/env python3.6
import sys
 
args = sys.argv

for line in sys.stdin:
    line = line.strip()
    if len(line.split()) != 4:
        continue
    projectName, title, count, size  = line.split()
    if projectName != args[1]:
        continue
    print(title, "\t", count)
