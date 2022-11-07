#!/usr/bin/env python3

### Advent of Code - 2016 - Day 2

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

grid1 = [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]

# Part 1
# Try moving in the direction 'd' and avoid stepping outside
# the grid bounds (defined by size s)
def move(g, x, y, d, s):
    nx, ny = x, y
    if d == 'U':
        ny = max(ny-1,0)
    if d == 'R':
        nx = min(nx+1,s)
    if d == 'D':
        ny = min(ny+1,s)
    if d == 'L':
        nx = max(nx-1,0)    
    if not g[ny][nx]:
        nx, ny = x, y
    return nx, ny

def input_code(x, y, grid):
    bx, by = x, y   
    code = []
    for line in input_lines:
        for d in line:
            bx, by = move(grid, bx, by, d, len(grid)-1)
        code.append(grid[by][bx])
    return code

part1(input_code(1, 1, grid1))

# Part 2
grid2 = [
    [ None, None, 1, None, None ],
    [ None, 2, 3, 4, None ],
    [ 5, 6, 7, 8, 9 ],
    [ None, 'A', 'B', 'C', None ],
    [ None, None, 'D', None, None ]
    ]

part2(input_code(0, 2, grid2))
