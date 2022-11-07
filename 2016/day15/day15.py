#!/usr/bin/env python3

### Advent of Code - 2016 - Day 15

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

def mul_inv(a,b):
    b0 = b
    x0,x1 = 0,1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a,b = b,a%b
        x0,x1 = x1-q*x0,x0
    if x1 < x0:
        x1 += b0
    return x1

def chinese_remainder(n,a):
    sum = 0
    prod = functools.reduce(lambda a,b: a*b,n)
    for ni,ai in zip(n,a):
        p = prod // ni
        sum += ai * mul_inv(p,ni)*p
    return sum % prod

disc_positions = []
disc_offsets = []

for i,l in enumerate(input_lines):
    nums = list(map(int,re.findall(r"-?\d+",l)))
    disc_positions.append(nums[1])
    disc_offsets.append(nums[1]-(nums[3]+i+1)%nums[1])


print(disc_positions)
print(disc_offsets)

part1(chinese_remainder(disc_positions,disc_offsets))

disc_positions.append(11)
disc_offsets.append(11 - (0+len(disc_positions)))

part2(chinese_remainder(disc_positions,disc_offsets))