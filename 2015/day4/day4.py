#!/usr/bin/env python3

### Advent of Code - 2015 - Day 4

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import hashlib

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

secret = finput
ans = 1
while hashlib.md5((secret+str(ans)).encode()).hexdigest()[0:5] != '00000':
    ans += 1
part1(ans)

while hashlib.md5((secret+str(ans)).encode()).hexdigest()[0:6] != '000000':
    ans += 1
part2(ans)
