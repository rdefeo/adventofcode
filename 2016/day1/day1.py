#!/usr/bin/env python3

### Advent of Code - 2016 - Day 1

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

px, py = 0, 0
facing = 'N'
turn_right = { 'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N' }
turn_left =  { 'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N' }
turn = { 'R': turn_right, 'L': turn_left }

visited = set()
visited.add((px,py))
p2 = None
for dir in input_lines[0].split(','):
    dir = dir.strip()
    facing = turn[dir[0]][facing]
    dist = int(dir[1:])

    # print(f"{px},{py}: now facing {facing}, moving {dist} steps")
    if facing in 'NS':
        s = 1 if facing == 'S' else -1
        for d in range(dist):
            py += s
            if (px,py) in visited and not p2:
                p2 = abs(px)+abs(py)
            visited.add((px,py))
    if facing in 'EW':
        s = 1 if facing == 'E' else -1
        for d in range(dist):
            px += s
            if (px,py) in visited and not p2:
                p2 = abs(px)+abs(py)
            visited.add((px,py))
     
part1(abs(px)+abs(py))
part2(p2)

