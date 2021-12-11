#!/usr/bin/env python3

### Advent of Code - 2021 - Day 11

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
# input_nums = list(map(int,input_lines))

X, Y = len(input_lines[0]), len(input_lines)
grid = dict()
for y,line in enumerate(input_lines):
    for x,v in enumerate(line):
        grid[(x,y)] = int(v)

DX = [1,1,0,-1,-1,-1,0,1]
DY = [0,1,1,1,0,-1,-1,-1]

total_flashes = 0
for s in itertools.count(1):
    grid = {k:v+1 for k,v in grid.items()} # gain energy
    flashers = [k for k,v in grid.items() if v > 9] # find flashers

    while flashers:
        for x,y in flashers:
            for i in range(8):
                nx, ny = x+DX[i], y+DY[i]
                if 0 <= nx < X and 0 <= ny < Y and grid[(nx,ny)] != 0:
                    # only increment non-zero octopi, they've already flashed!
                    grid[(nx,ny)] += 1
            grid[(x,y)] = 0 # set flashed octopi to zero
        # we flashed all the octopus that reached max energy, now check if we made more
        flashers = [k for k,v in grid.items() if v > 9]
    total_flashes += sum(v == 0 for v in grid.values())
    if s == 100:
        part1(total_flashes)
    if all(v==0 for v in grid.values()):
        part2(s)
        break
