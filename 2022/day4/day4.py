#!/usr/bin/env python3

### Advent of Code - 2022 - Day 4

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
#input_nums = list(map(int,input_lines))

contains = 0
overlaps = 0
for p in input_lines:
    m = re.findall(r'\d+',p)
    a,b,x,y = list(map(int,m))
    # print(a,b,x,y)
    if a <= x and y <= b:
        contains += 1
    elif x <= a and b <= y:
        contains += 1

    if a <= x <= b or a <= y <= b:
        overlaps += 1
    elif x <= a <= y or x <= b <= y:
        overlaps += 1
part1(contains)
part2(overlaps)

