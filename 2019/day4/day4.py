#!/usr/bin/env python3

### Advent of Code - 2019 - Day 4

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

p1, p2 = list(map(int,finput.split('-')))

def count_passwords(part2=False):
    valid = 0
    for p in range(p1,p2+1):
        if not all(a<=b for a,b in zip(str(p),str(p)[1:])):
            continue
        c = collections.Counter(str(p))
        if c.most_common(1)[0][1] < 2: # doubles?
            continue
        if part2 and not any(n[1]==2 for n in c.most_common()):
            continue
        valid += 1
    return valid

part1(count_passwords())
part2(count_passwords(True))