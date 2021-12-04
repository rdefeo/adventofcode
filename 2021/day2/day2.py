#!/usr/bin/env python3

### Advent of Code - 2021 - Day 2

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

H, D = 0, 0
for cmd in input_lines:
    d, a = cmd.split()
    a = int(a)
    if d == 'forward':
        H += a
    elif d == 'down':
        D += a
    elif d == 'up':
        D -= a
part1(H*D)

H, D, A = 0, 0, 0
for cmd in input_lines:
    d, a = cmd.split()
    a = int(a)
    if d == 'forward':
        H += a
        D += A*a
    elif d == 'down':
        A += a
    elif d == 'up':
        A -= a
part2(H*D)
