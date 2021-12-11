#!/usr/bin/env python3

### Advent of Code - 2015 - Day 24

import sys, requests, re, math, itertools, functools, os, collections, operator
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

packages = list(map(int,input_lines))

# packages = [1,2,3,4,5,7,8,9,10,11]
# print(sum(packages)//3)

target = sum(packages)//4 # part1 = 3

# with ever increasing package counts (x)
for x in range(2,len(packages)):
    qe = []
    # get all combinations of that length (x)
    for p in itertools.combinations(packages,x):
        if sum(p) == target:
            # and compute the 'quantum entanglement' (product) of those packages
            qe.append(functools.reduce(operator.mul,p))
    # if we had valid lists of length (x), return the munimum 'qe' found
    if len(qe):
        part1(min(qe))
        break
