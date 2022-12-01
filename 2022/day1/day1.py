#!/usr/bin/env python3

### Advent of Code - 2022 - Day 1

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

# original code
m = []
for cal in finput.split('\n\n'):
    # print(cal)
    s = 0
    for c in cal.split('\n'):
        s += int(c)
    m.append(s)
part1(max(m))

# one-liner
# m = [sum(int(c) for c in cal.split('\n')) for cal in finput.split('\n\n')]
# part1(max(m))


part2(sum(sorted(m,reverse=True)[:3]))
