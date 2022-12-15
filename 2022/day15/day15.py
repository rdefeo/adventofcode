#!/usr/bin/env python3

### Advent of Code - 2022 - Day 15

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
finput = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in finput.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


tunnels = dict() # { sensor : beacon }
for line in input_lines:
    sx,sy,bx,by = list(map(int,re.findall(r'([-\d]+)',line)))
    tunnels[(sx,sy)] = (bx,by)

def mdist(s,b):
    return (abs(s[0]-b[0])+abs(s[1]-b[1]))

# { sensor : Manhattan distance }
dists = { s: mdist(s,b) for s,b in tunnels.items() }

# Part 1
# compute sensor range map for the selected row 'p1_y_value'
# we only need to compute the range if the distance between s and b
# will take us in range of the 'p1_y_value'

sensor_range = set()
p1_y_value = 2_000_000
# p1_y_value = 10
left = 1e10
right = -1e10

for s,d in dists.items():
    if p1_y_value-d <= s[1] <= p1_y_value+d: # are we close enough to the p1_y_value line?
        ygap = abs(s[1]-p1_y_value)
        for x in range(s[0]-d+ygap,s[0]+d-ygap+1):
            sensor_range.add(x)
            left = min(left,x)
            right = max(right,x)

num_beacons = len(set(b for b in tunnels.values() if b[1] == p1_y_value))
part1(len(sensor_range) - num_beacons)


# Part 2
# compute the edge locations for each sensor, our distress signal
# must be coming from one of them. for every edge, check if it's
# inside any of the other sensor ranges, if not - we're done

p2_range = 4_000_000
# p2_range = 20
for s,d in dists.items():
    y1 = max(0,s[1]-d-1)
    y2 = min(p2_range,s[1]+d+1)
    for y in range(y1,y2+1):
        xgap = d - abs(s[1]-y)
        x1 = s[0]-xgap-1
        x2 = s[0]+xgap+1
        for x in [x1, x2]:
            if x < 0 or x > p2_range: continue
            if all(mdist((x,y),s1) > d1 for s1,d1 in dists.items()):
                print((x,y))
                part2(x*4_000_000 + y)
                exit()
