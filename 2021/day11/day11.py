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

def step(g,s):
    g = {k:v+1 for k,v in g.items()} # gain energy
    flashers = [k for k,v in g.items() if v > 9] # find flashers

    while flashers:
        for x,y in flashers:
            for i in range(8):
                nx, ny = x+DX[i], y+DY[i]
                if 0 <= nx < X and 0 <= ny < Y and g[(nx,ny)] != 0:
                    # only increment non-zero octopi, they've already flashed!
                    g[(nx,ny)] += 1
            g[(x,y)] = 0 # set flashed octopi to zero
        # we flashed all the octopus that reached max energy, now check if we made more
        flashers = [k for k,v in g.items() if v > 9]
    if all(v==0 for v in g.values()):
        part2(s+1)
        exit()
    return g, sum(v == 0 for v in g.values())

# Part 1
g = grid
fc = 0
for s in range(100):
    g,f = step(g,s)
    fc += f
part1(fc)

# Part 2
g = grid
for s in range(10000):
    g,_ = step(g,s)
