#!/usr/bin/env python3

### Advent of Code - 2024 - Day 2

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

# are all consecutive levels increasing or decreasing by 1..3?
def is_safe(l):
    return all([1 <= a-b <= 3 for a,b in zip(l,l[1:])]) or all([1 <= b-a <= 3 for a,b in zip(l,l[1:])])

safe = 0
safe2 = 0
for report in input_lines:
    levels = list(map(int,report.split()))
    if is_safe(levels):
        safe += 1
    else:
        # not a safe report, so let's try removing a single element and check again
        for i in range(len(levels)):
            levels2 = levels[:i] + levels[i+1:]
            if is_safe(levels2):
                safe2 += 1
                # stop checking, as a report might be safe if we remove more than one level
                # and we don't want to count it multiple times
                break
part1(safe)

# report the original safe plus the ones deemed safe by dampening
part2(safe2+safe)
