#!/usr/bin/env python3

### Advent of Code - 2024 - Day 11

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

stones = list(map(int,finput.split()))

# Apply the rules to a single stone, caching repeated calls
blink_seen = dict()
def blink(s):
    if s in blink_seen:
        return blink_seen[s]
    new_stones = []
    if s == 0:
        new_stones.append(1)
    elif len(str(s)) % 2 == 0:
        length = len(str(s))
        new_stones.append(int(str(s)[:length//2]))
        new_stones.append(int(str(s)[length//2:]))
    else:
        new_stones.append(s*2024)
    blink_seen[s] = new_stones
    return new_stones

# Start with a count of our stones
cnt = collections.Counter(stones)
print(cnt)
for b in range(75):
    if b == 25:
        part1(sum(cnt.values()))
    cnt2 = cnt.copy()
    # For every stone in our counter, decrement the count, blink it,
    # then increment the resulting new stones
    for s in cnt:
        cnt2[s] -= cnt[s]
        res = blink(s)
        for ns in res:
            cnt2[ns] += cnt[s]
    cnt = cnt2.copy()
part2(sum(cnt.values()))
