#!/usr/bin/env python3

### Advent of Code - 2016 - Day 13

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from heapq import heappush, heappop

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

def neighbors(x,y):
    directions = [(1,0),(0,1),(-1,0),(0,-1)] # R,D,L,U
    return [(x+d[0],y+d[1]) for d in directions]

tx,ty = 31,39
# tx,ty = 7,4 # sample
visited = {(1,1):0 } # pos: dist

def is_wall(x,y):
    v = x*x + 3*x + 2*x*y + y + y*y + 1350 # 10 # sample
    return bin(v).count('1')%2 == 1

heap = [(0,(1,1))] # dist,(x,y)
while True:
    dist,(x,y) = heappop(heap)
    if (x,y) == (tx,ty):
        part1(dist)
        break
    dist += 1
    for nx,ny in neighbors(x,y):
        if nx < 0 or ny < 0:
            continue
        if is_wall(nx,ny):
            continue
        if (nx,ny) in visited and visited[(nx,ny)] <= dist:
            continue
        visited[(nx,ny)] = dist
        heappush(heap,(dist,(nx,ny)))

# locations we can visit in at most 50 steps
part2(sum([v<=50 for k,v in visited.items()]))
