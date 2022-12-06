#!/usr/bin/env python3

### Advent of Code - 2022 - Day 5

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

def read_stacks():
    st = [[] for _ in range(9)]
    for i in range(7,-1,-1):
        for s in range(1,len(input_lines[i]),4):
            # print(input_lines[i][s],end=' ')
            if input_lines[i][s].isupper():
                st[(s-1)//4].append(input_lines[i][s])
        # print()
    return st

# Part 1
stacks = read_stacks()
print(stacks)
for i in range(10, len(input_lines)):
    amt, fr, to = list(map(int,re.findall(r'\d+',input_lines[i])))

    for a in range(amt):
        c = stacks[fr-1].pop(-1)
        stacks[to-1].append(c)
part1(''.join(s[-1] for s in stacks))

# Part 2
stacks = read_stacks()
for i in range(10, len(input_lines)):
    amt, fr, to = list(map(int,re.findall(r'\d+',input_lines[i])))

    c = stacks[fr-1][-amt:]
    stacks[fr-1] = stacks[fr-1][:-amt]
    stacks[to-1] += c
part2(''.join(s[-1] for s in stacks))
