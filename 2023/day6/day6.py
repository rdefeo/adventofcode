#!/usr/bin/env python3

### Advent of Code - 2023 - Day 6

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
#input_nums = list(map(int,input_lines))

times = list(map(int,input_lines[0].split()[1:]))
dists = list(map(int,input_lines[1].split()[1:]))

total_ways = []
for i, t in enumerate(times):
    ways = 0
    for h in range(1,t-1):
        d = h * (t-h)
        if d > dists[i]:
            ways += 1
    total_ways.append(ways)
part1(functools.reduce(lambda x, y: x*y, total_ways))

time = int(''.join(list(map(str,times))))
dist = int(''.join(list(map(str,dists))))

ways = 0
for h in range(1,time-1):
    d = h * (time-h)
    if d > dist:
        ways += 1
part2(ways)