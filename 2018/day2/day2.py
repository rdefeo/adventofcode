#!/usr/bin/env python3

### Advent of Code - 2018 - Day 2

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
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

def count_N_repeats(n):
    boxes = 0
    for x in input_lines:
        c = collections.Counter(x)
        for v in c.values():
            if v == n:
                boxes += 1
                break
    return boxes

part1(count_N_repeats(2) * count_N_repeats(3))

for b in input_lines:
    for c in input_lines:
        if b == c:
            continue
        diffs = 0
        for i in range(len(b)):
            if b[i] != c[i]:
                diffs += 1
        if diffs == 1:
            box_diff = ''
            for i in range(len(b)):
                if b[i] == c[i]:
                    box_diff += b[i]
            part2(box_diff)
            quit()
