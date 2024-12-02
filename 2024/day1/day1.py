#!/usr/bin/env python3

### Advent of Code - 2024 - Day 1

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

list_a, list_b = [], []
for line in input_lines:
    a, b = list(map(int, line.split()))
    list_a.append(a)
    list_b.append(b)
# print(len(list_a),len(list_b))
part1(sum(abs(a-b) for a,b in zip(sorted(list_a),sorted(list_b))))

bcounts = collections.Counter(list_b)
similarity = 0
for loc in list_a:
    similarity += loc * bcounts[loc]
part2(similarity)
