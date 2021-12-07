#!/usr/bin/env python3

### Advent of Code - 2021 - Day 7

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

crabs = [int(c) for c in finput.split(',')]

def compute_fuel(crabs,fuel_func):
    cheapest = 99999999999999
    # naive solution: try each possible position for the alignment
    # and return the cheapest
    for p in range(min(crabs),max(crabs)+1):
        cheapest = min(cheapest,sum(fuel_func(c-p) for c in crabs))
    return int(cheapest)

# fuel cost is simply the (positive) distance between the crab and our pivot
part1(compute_fuel(crabs,abs))

# for part 2, it's the sum of all digits between 1..distance to pivot
part2(compute_fuel(crabs,lambda x: abs(x)*(abs(x)+1)/2))
