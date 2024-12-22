#!/usr/bin/env python3

### Advent of Code - 2024 - Day 22

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

secrets = list(map(int,input_lines))

def mix_and_prune(n):
    n = (n ^ (n << 6)) % 16777216
    n = (n ^ (n >> 5)) % 16777216
    n = (n ^ (n << 11)) % 16777216
    return n

# Part 1
# Simply apply the mix and prune process on every initial secret
# Do some bookeeping for Part 2, so we don't have to recalc the secrets again
#  Along the way, keep track of the differences of the 1's digit
#  For each secret number, store the number of bananas for ever difference sequence
total = 0
seq = [] # secret -> dict[ sequence ] = banana num
for s in secrets:
    nums = [s%10]
    diffs = []
    for _ in range(2000):
        s = mix_and_prune(s)
        nums.append(s%10)
        diffs.append(nums[-1]-nums[-2])
    total += s

    ns = dict()
    for i in range(len(diffs)-3):
        d = tuple(diffs[i:i+4])
        if d not in ns: # ensures we only use the num bananas for the first occurrence of seq
            ns[d] = nums[i+4]
    seq.append(ns)
part1(total)

# Part 2
# For all unique difference sequences, find the one that produces the most bananas
banana_cnt = collections.defaultdict(int)
for s in seq:
    for sq,b in s.items():
        banana_cnt[sq] += b
part2(max(banana_cnt.values()))

