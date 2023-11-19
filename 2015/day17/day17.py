#!/usr/bin/env python3

### Advent of Code - 2015 - Day 17

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

print(input_nums)

# Generate all combinations of our containers, starting with at least 2
# Compute the sum and add to our nog_count. Also keep track of the number of containers
# that had a matching total in the size_count dict.
total_nog = 150
nog_count = 0
size_count = collections.defaultdict(int)
for l in range(2, len(input_nums)):
    for c in itertools.combinations(range(len(input_nums)), l):
        s = sum(input_nums[i] for i in c)
        if s == total_nog:
            nog_count += 1
            size_count[l] += 1
part1(nog_count)
part2(size_count[min(size_count)])
