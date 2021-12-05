#!/usr/bin/env python3

### Advent of Code - 2021 - Day 5

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

# returns -1, 0, 1
def sign(x):
    return (x>0)-(x<0)

# draw lines for both parts
def draw_lines():
    vents1 = collections.defaultdict(int)
    vents2 = collections.defaultdict(int)
    for line in input_lines:
        x1,y1,x2,y2 = map(int,re.findall(r'\d+',line))
        sx, sy = sign(x2-x1), sign(y2-y1)          # get slope increment
        dist = max(abs(x2-x1),abs(y2-y1))          # total distance
        for p in range(dist+1):
            vents2[(x1+(sx*p),y1+(sy*p))] += 1     # part2 draws all lines
            if sx == 0 or sy == 0:                 # part1 only draws horizontal or vertical
                vents1[(x1+(sx*p),y1+(sy*p))] += 1
    return vents1, vents2

v1, v2 = draw_lines()
part1(sum([v>=2 for v in v1.values()]))
part2(sum([v>=2 for v in v2.values()]))