#!/usr/bin/env python3

### Advent of Code - 2021 - Day 1

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
larger = 0
for i in range(1,len(input_nums)):
    # print(f"{input_nums[i-1]} < {input_nums[i]}")
    if input_nums[i-1] < input_nums[i]:
        larger += 1
part1(larger)

larger = 0
for i in range(3,len(input_nums)):
    # print(f"{input_nums[i-4:i-1]} < {input_nums[i-3:i]}")
    if sum(input_nums[i-4:i-1]) < sum(input_nums[i-3:i]):
        larger += 1
part2(larger)




