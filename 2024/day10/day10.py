#!/usr/bin/env python3

### Advent of Code - 2024 - Day 10

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

topo = dict()
trailheads = []
for y, row in enumerate(input_lines):
    for x, alt in enumerate(row):
        alt = int(alt)
        topo[(x,y)] = alt
        if alt == 0:
            trailheads.append((x,y))

def find_trails(th, p2=False):
    score = 0
    paths = [th]
    ends = set()
    while paths:
        th = paths.pop(0)
        if topo[th] == 9:
            if p2 or th not in ends:
                score += 1
                ends.add(th)
            continue
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            nth = (th[0]+dx,th[1]+dy)
            if nth in topo and topo[nth] == topo[th]+1:
                paths.append(nth)
    return score

total1, total2 = 0, 0
for th in trailheads:
    total1 += find_trails(th)
    total2 += find_trails(th,True)
part1(total1)
part2(total2)
