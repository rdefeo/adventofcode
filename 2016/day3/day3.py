#!/usr/bin/env python3

### Advent of Code - 2016 - Day 3

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

# Part 1
def is_triangle(a, b, c):
    return int(a+b>c and b+c > a and a+c > b)

possible = 0
for t in input_lines:
    a, b, c = map(int,t.split())
    possible += is_triangle(a,b,c)
part1(possible)

# Part 2
# Need to transpose the input data, then loop over the 3 lists, by 3s
possible = 0
nt = [ [], [], [] ]
for t in input_lines:
    a, b, c = map(int,t.split())
    nt[0].append(a)
    nt[1].append(b)
    nt[2].append(c)
for t in nt:
    for j in range(0,len(t),3):
        possible += is_triangle(t[j],t[j+1],t[j+2])
part2(possible)
