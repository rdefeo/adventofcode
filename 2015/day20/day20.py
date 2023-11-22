#!/usr/bin/env python3

### Advent of Code - 2015 - Day 20

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
input_num = int(input_lines[0])

def get_divisors(n):
    """ Generic get divisors method from the internet """
    factors = {1}
    maxP = math.isqrt(n)
    p, inc = 2, 1
    while p <= maxP:
        while n % p == 0:
            factors.update([f*p for f in factors])
            n //= p
            maxP = math.isqrt(n)
        p, inc = p + inc, 2
    if n > 1:
        factors.update([f*n for f in factors])
    return sorted(factors) # really doesn't need to be sorted

def get_presents(house):
    return sum(d * 10 for d in get_divisors(house))

h = 500000
while get_presents(h) < input_num:
    h += 1
part1(h)

def get_presents2(house):
    sum = 0
    divs = get_divisors(house)
    for d in divs:
        # Add, only if we didn't visit more than 50 houses
        if house / d <= 50:
            sum += d
    return sum * 11

h = 500000
while get_presents2(h) < input_num:
    h += 1
part2(h)

