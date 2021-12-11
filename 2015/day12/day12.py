#!/usr/bin/env python3

### Advent of Code - 2015 - Day 12

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import json

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

# Part 1
part1(sum([int(n) for n in re.findall(r"-?\d+",input_lines[0])]))

# Part 2
def find_numbers(j):
    if isinstance(j, list):
        return sum([find_numbers(item) for item in j])
    elif isinstance(j, int):
        return j
    elif isinstance(j, str):
        return 0
    else: # is dict
        s = 0
        for v in j.values():
            if v == "red":
                return 0
            if isinstance(v, int):
                s += v
            elif isinstance(v, list) or isinstance(v, dict):
                s += find_numbers(v)
        return s

for line in input_lines:
    s = find_numbers(json.loads(line))
    part2(s)
