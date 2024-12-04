#!/usr/bin/env python3

### Advent of Code - 2024 - Day 4

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

width = len(input_lines[0])
height = len(input_lines)

# Compute the list of coordinates (of length l) in all 8 directions
# or just for the diagonals, starting at x,y
def gen_coords(x,y,l,diag_only=False):
    dirs = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]
    if diag_only:
        dirs = dirs[:4]
    for d in dirs:
        coords = [(x+d[0]*i,y+d[1]*i) for i in range(l)]
        if all(0 <= c[0] < width and 0 <= c[1] < height for c in coords):
            yield coords

# For every X, check the directions for XMAS
count = 0
for y in range(height):
    for x in range(width):
        if input_lines[y][x] == 'X':
            for c in gen_coords(x,y,4):
                if input_lines[c[1][1]][c[1][0]] == 'M' \
                    and input_lines[c[2][1]][c[2][0]] == 'A' \
                        and input_lines[c[3][1]][c[3][0]] == 'S':
                    count += 1
part1(count)

# For every MAS, count the locations of A.
# Every coordinate that's counted twice means we have two MAS's intersecting
mas = collections.defaultdict(int)
for y in range(height):
    for x in range(width):
        if input_lines[y][x] == 'M':
            for c in gen_coords(x,y,3,True):
                if input_lines[c[1][1]][c[1][0]] == 'A' \
                    and input_lines[c[2][1]][c[2][0]] == 'S':
                    mas[c[1]] += 1
part2(sum(v == 2 for v in mas.values()))    
