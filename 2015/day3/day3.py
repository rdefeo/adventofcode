#!/usr/bin/env python3

### Advent of Code - 2015 - Day 3

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


M = {'>':(1,0), 'v':(0,1), '<':(-1,0), '^':(0,-1)}

s = collections.defaultdict(int)
x, y = 0, 0
s[(x,y)] = 1
for d in finput:
    m = M[d]
    x += m[0]
    y += m[1]
    s[(x,y)] += 1
part1(len(s))

s.clear()
r = collections.defaultdict(int)
sx, sy = 0, 0
s[(sx,sy)] = 1
rx, ry = 0, 0
r[(rx,ry)] = 1
for i, d in enumerate(finput):
    m = M[d]
    if i%2 == 0:
        sx += m[0]
        sy += m[1]
        s[(sx,sy)] += 1
    else:
        rx += m[0]
        ry += m[1]
        r[(rx,ry)] += 1
part2(len(set(s)|set(r)))
