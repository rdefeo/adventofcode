#!/usr/bin/env python3

### Advent of Code - 2024 - Day 18

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq

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

bytes = [tuple(int(num) for num in line.split(",")) for line in input_lines]

# Change these depending on input being tested
SIZE = 71
BYTE_CNT = 1024

def print_grid(grid):
    for y in range(SIZE):
        for x in range(SIZE):
            print(grid[(x,y)],end='')
        print()
    print()

# Dijkstra's algorithm
def find_path(S, E, grid: dict) -> tuple:
    queue = [(0, S, [])] # path len, pos, path
    seen = set()
    path_lens = collections.defaultdict(int)
    while queue:
        path_len, p1, path = heapq.heappop(queue)
        if p1 in seen: continue
        seen.add(p1)
        path = [p1] + path
        if p1 == E: return (path_len, path)

        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            np = (p1[0]+dx,p1[1]+dy)
            if np in seen: continue
            if grid[np] == '#': continue
            if 0 <= np[0] <= E[0] and 0 <= np[1] <= E[1]:
                prev = path_lens[np]
                next = path_len + 1
                if prev == 0 or next < prev:
                    path_lens[np] = next
                    heapq.heappush(queue, (next, np, path))
    return float("inf"), None

# Fill a blank grid with a number of bytes
grid = collections.defaultdict(lambda:'.')
for b in range(BYTE_CNT):
    grid[bytes[b]] = '#'
#print_grid(grid)

# Part 1
path_len, path = find_path((0,0),(SIZE-1,SIZE-1),grid)
# print(path_len, path)
part1(path_len)

# Part 2
# Starting from our last good byte count, keep adding one by one
# until we fail to find a path. Brute force works just fine... :)
for b in range(BYTE_CNT+1,len(bytes)+1):
    grid[bytes[b]] = '#'
    path_len, path = find_path((0,0),(SIZE-1,SIZE-1),grid)
    if path == None:
        part2(bytes[b])
        break