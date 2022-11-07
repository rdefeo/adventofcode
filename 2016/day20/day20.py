#!/usr/bin/env python3

### Advent of Code - 2016 - Day 20

import sys, requests, re, math, itertools, functools, os, collections
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

ranges = []
for line in input_lines:
    l,r = list(map(int,line.split('-')))
    ranges.append((l,r))



def overlap(a,b):
    if a[1] < b[0] or a[0] > b[1]:
        return None
    return (min(a[0],b[0]),max(a[1],b[1]))

ranges.sort()
print(ranges)

part_1 = False
r = 0
ip = 0
total = 0
while ip < 2**32:
    (lo,hi) = ranges[r]
    if ip >= lo:
        if ip <= hi:
            ip = hi + 1
            continue
        r += 1
    else:
        # if part_1:
        #     part1(ip)
        #     break
        total += 1
        ip += 1

part2(total)

