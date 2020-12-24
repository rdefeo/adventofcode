#!/usr/bin/env python3

### Advent of Code - 2018 - Day 3

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

fabric = collections.defaultdict(int)

overlaps = set()
claims = set()
for claim in input_lines:
    m = list(map(int,re.findall(f"\d+",claim)))

    claims.add(m[0])
    for x in range(m[3]):
        for y in range(m[4]):
            p = (m[1]+x,m[2]+y)
            if p in fabric:
                if fabric[p] != 'X':
                    overlaps.add(fabric[p])
                overlaps.add(m[0])
                fabric[p] = 'X'
            else:
                fabric[p] = m[0]
#print(fabric)
part1(sum(v=='X' for v in fabric.values()))

part2(claims ^ overlaps)