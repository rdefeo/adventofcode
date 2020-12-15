#!/usr/bin/env python3

### Advent of Code - 2020 - Day 13

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
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
#input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


timestamp = int(input_lines[0])
all_ids = input_lines[1].split(',')
bus_ids = [int(x) for x in input_lines[1].split(',') if x != 'x']

print(timestamp)
print(bus_ids)

start_timer('part 1')

next_bus_wait = sorted([(b-(timestamp%b),b) for b in bus_ids])
print(next_bus_wait)
part1(next_bus_wait[0][0]*next_bus_wait[0][1])

stop_timer('part 1')


offsets = [int(b)-i for i,b in enumerate(all_ids) if b != 'x']

def chinese_remainder(n, a):
    sum = 0
    prod = functools.reduce(lambda a,b: a*b, n)
    for ni,ai in zip(n,a):
        p = prod // ni
        sum += ai * mul_inv(p,ni)*p
    return sum % prod

def mul_inv(a,b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1-q*x0, x0
    if x1 < 0:
        x1 += b0
    return x1   

# n = [3,5,7]
# a = [2,3,2]
# print(chinese_remainder(n,a))

# n = [17,13,19]
# a = [0,11,16]
# print(chinese_remainder(n,a))

offsets[0] = 0
print(f"Ids: {bus_ids}")
print(f"Off: {offsets}")
start_timer('part 2: CRT')
part2(chinese_remainder(bus_ids,offsets))
stop_timer('part 2: CRT')

start_timer('another sol')
t = 0
rp = 1
for i,b in enumerate(all_ids):
    if b == 'x':
        continue
    while (t+i)%int(b) != 0:
        t += rp
    rp *= int(b)
part2(t)
stop_timer('another sol')

