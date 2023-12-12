#!/usr/bin/env python3

### Advent of Code - 2023 - Day 10

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


spos = ()
grid = collections.defaultdict(lambda : '.')
for row, line in enumerate(input_lines):
    for col, p in enumerate(line):
        grid[(col,row)] = p
        if p == 'S':
            spos = (col,row)


NORTH, EAST, SOUTH, WEST = (0,-1),(1,0),(0,1),(-1,0)

NEXT_DIR = {
    '|': {NORTH: NORTH, SOUTH: SOUTH},
    '-': {EAST: EAST, WEST: WEST},
    'L': {SOUTH: EAST, WEST: NORTH},
    'J': {SOUTH: WEST, EAST: NORTH},
    '7': {EAST: SOUTH, NORTH: WEST},
    'F': {WEST: SOUTH, NORTH: EAST}
}

# Determine our starting 'dir' by checking neighboring pipes
dir = None
avail_dirs = []
for d in [NORTH,EAST,SOUTH,WEST]:
    npos = (spos[0]+d[0],spos[1]+d[1])
    if npos in grid and grid[npos] in NEXT_DIR and d in NEXT_DIR[grid[npos]]:
        avail_dirs.append(d)
# Given all available directions of travel from 'S', replace 'S' with appropriate
# pipe symbol
for p in NEXT_DIR:
    if all(a in NEXT_DIR[p].values() for a in avail_dirs):
        grid[spos] = p
        break
print(f"Starting position is pipe {grid[spos]}")

path = [] # list of path vertices - used for Part 2
if grid[spos] in "LJ7F":
    path.append(spos)
dir = avail_dirs[0] # pick any starting direction

npos = (spos[0]+dir[0],spos[1]+dir[1])
steps = 1
while npos != spos:
    if grid[npos] in "LJ7F":
        path.append(npos)
    pipe = grid[npos]
    dir = NEXT_DIR[pipe][dir]
    npos = (npos[0]+dir[0],npos[1]+dir[1])
    steps += 1
part1(steps // 2)

def get_real_intersections(ints):
    # we only care about segment intersections that are: |, L-7, F-J
    # intersections with segments that are F-7 or L-J don't count towards area
    rints = []
    for i in sorted(ints):
        a, b = ints[i]
        if a[0] == b[0]: # |
            rints.append(a[0])
        elif grid[a] == 'L' and grid[b] == '7':
            rints.append(a[0])
        elif grid[a] == 'F' and grid[b] == 'J':
            rints.append(a[0])
    return rints

area = 0
for y in range(len(input_lines)):
    narea = 0
    ints = dict() # all intersections, whether vert or horiz
    for a,b in zip(path,path[1:]+[path[0]]):
        if y == a[1] == b[1]:
            ints[min(a[0],b[0])] = (a,b) if a[0] < b[0] else (b,a)
        elif (a[1] < y < b[1]) or (b[1] < y < a[1]):
            ints[a[0]] = (a,b)
    if not ints:
        continue
    rints = get_real_intersections(ints)
    if len(rints) and len(rints) % 2 == 0:
        horiz = sorted(set(ints)-set(rints))
        pairs = [(rints[i],rints[i+1]) for i in range(0,len(rints),2)]
        for a,b in pairs:
            ia = ints[b][0][0] - ints[a][1][0] - 1
            if ia:
                for m in range(a+1,b):
                    if m in horiz:
                        ia -= (ints[m][1][0] - ints[m][0][0] + 1)
            narea += ia

    area += narea
part2(area)
