#!/usr/bin/env python3

### Advent of Code - 2018 - Day 20

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

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

R = input_lines[0]

d = { 'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1) }

positions = []
x,y = 9999,9999
m = collections.defaultdict(set)
py,px = y,x
distances = collections.defaultdict(int)
dist = 0
for c in R[1:-1]:
    if c == '(':
        positions.append((y,x))
    elif c == ')':
        y,x = positions.pop()
    elif c == '|':
        y,x = positions[-1]
    else:
        dy,dx = d[c]
        y += dy
        x += dx
        m[(y,x)].add((py,px))
        if distances[(y,x)] != 0:
            distances[(y,x)] = min(distances[(y,x)], distances[(py,px)]+1)
        else:
            distances[(y,x)] = distances[(py,px)]+1
    py,px = y,x
part1(max(distances.values()))
part2(len([d for d in distances.values() if d >= 1000]))
