#!/usr/bin/env python3

### Advent of Code - 2015 - Day 16

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

sues = []
for line in input_lines:
    m = re.search(r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)", line)
    sues.append({ m[i]: int(m[i+1]) for i in range(2,7,2) })

SUE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

for i, s in enumerate(sues):
    match = True
    for k,v in s.items():
        if k in SUE:
            if SUE[k] != v:
                match = False
                break
    if match:
        part1(f"{i+1}, {s}")
        break

for i, s in enumerate(sues):
    match = True
    for k,v in s.items():
        if k in SUE:
            if k in ['cats', 'trees']:
                if v <= SUE[k]:
                    match = False
                    break
            elif k in ['pomeranians', 'goldfish']:
                if v >= SUE[k]:
                    match = False
                    break
            elif SUE[k] != v:
                match = False
                break
    if match:
        part2(f"{i+1}, {s}")
        break