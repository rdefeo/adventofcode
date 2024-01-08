#!/usr/bin/env python3

### Advent of Code - 2019 - Day 1

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
input_nums = list(map(int,input_lines))

# Part 1
part1(sum([(m//3)-2 for m in input_nums]))

# Part 2
fuel = 0
for m in input_nums:
    f = m//3 - 2
    if f > 0:
        fuel += f
        while True:
            f = f//3 - 2
            if f <= 0: break
            fuel += f
part2(fuel)
