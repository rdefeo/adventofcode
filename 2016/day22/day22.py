#!/usr/bin/env python3

### Advent of Code - 2016 - Day 22

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

min_used = 9999
max_avail = 0

max_x = 0
max_y = 0
nodes = {}
for i in input_lines:
    m = list(map(int,re.findall(r"\d+",i)))
    if m:
        x,y,s,u,a,p = m
        min_used = min(min_used,u)
        max_avail = max(max_avail,a)
        nodes[(x,y)] = [s,u,a,p]
        max_x = max(max_x,x)
        max_y = max(max_y,y)

def count_pairs(nodes):
    c = 0
    for a in nodes:
        for b in nodes:
            if a == b: continue
            if nodes[a][1] and nodes[b][2] > nodes[a][1]:
                c += 1
    return c

part1(count_pairs(nodes))

# Part 2 - print the map and count by hand
#  1. count the number of moves to move the 'hole' up to the top-right
#  2. count how many moves left we need to move the 'data'. multiply by 5
#  Answer is #1 + #2 * 5
for y in range(max_y+1):
    for x in range(max_x+1):
        n = nodes[(x,y)]
        print(f"{n[1]}".center(4),end='')
    print('')