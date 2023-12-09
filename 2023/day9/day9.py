#!/usr/bin/env python3

### Advent of Code - 2023 - Day 9

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

history = [list(map(int,line.split())) for line in input_lines]

next_hist = []
prev_hist = []
for h in history:
    # For each list of historical values, keep generating a list of diffs
    # until the all of the diffs are zero
    # Turns [1, 3, 6, 10, 15, 21] into this
    # [[1, 3, 6, 10, 15, 21], [2, 3, 4, 5, 6], [1, 1, 1, 1], [0, 0, 0]]
    diffs = [h]
    while any(d != 0 for d in diffs[-1]):
        next_diffs = [b-a for a,b in zip(diffs[-1],diffs[-1][1:])]
        diffs.append(next_diffs)
    print(diffs)

    # Find next value for Part 1
    # Simply sum the last value of every diff list
    next_hist.append(sum(d[-1] for d in diffs))

    # Find prev value for Part 2
    # Walk our diffs list backwards and continually take the difference of
    # the first value in each diff list to get our prev value
    prev_hist.append(functools.reduce(lambda a,b: b-a,[d[0] for d in diffs[::-1]]))

part1(sum(next_hist))
part2(sum(prev_hist))

