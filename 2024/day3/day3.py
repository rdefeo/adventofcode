#!/usr/bin/env python3

### Advent of Code - 2024 - Day 3

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

# find all mul(X,Y) and sum
mul = r"mul\((\d{1,3}),(\d{1,3})\)"
total = 0
m = re.findall(mul,finput)
for i in m:
    total += int(i[0]) * int(i[1])
part1(total)

# this time, find all mul(X,Y), do(), and don't()
total = 0
do_flag = True
mul = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
for m in re.findall(mul,finput):
    if m == "don't()":
        do_flag = False
    elif m == "do()":
        do_flag = True
    else:
        if do_flag:
            x, y = map(int, m[4:-1].split(','))
            total += x*y
part2(total)
