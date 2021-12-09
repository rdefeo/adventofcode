#!/usr/bin/env python3

### Advent of Code - 2021 - Day 9

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache, reduce

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

cfloor = collections.defaultdict(int)
max_y = len(input_lines)
max_x = len(input_lines[0])
for y,line in enumerate(input_lines):
    for x,h in enumerate([int(f) for f in line]):
        cfloor[(x,y)] = h


# Part 1

# return iterable of neighbors in the grid
def get_neighbors(b):
    dir = [(1,0), (0,1), (-1,0), (0,-1)]
    for d in dir:
        dx, dy = b[0]+d[0], b[1]+d[1]
        if (0 <= dx < max_x) and (0 <= dy < max_y):
            yield((dx,dy)) 

# is point lower than neighbors?
def is_low_point(p,s):
    return all([s[p] < s[d] for d in get_neighbors(p)])

def find_low_points(s):
    return [(x,y) for x in range(max_x) for y in range(max_y) if is_low_point((x,y),s)]

part1(sum([cfloor[lp]+1 for lp in find_low_points(cfloor)]))


# Part 2

# BFS the grid from each low point until we hit a 9
def basin_size(start,s):
    queue = [start]
    in_basin = set([start])
    while queue:
        p = queue.pop(0)
        for n in get_neighbors(p):
            if n not in in_basin and s[n] != 9:
                queue.append(n)
                in_basin.add(n)
    return len(in_basin)

basin_sizes = [basin_size(lp,cfloor) for lp in find_low_points(cfloor)]
part2(reduce((lambda x,y: x*y),sorted(basin_sizes)[-3:]))


