#!/usr/bin/env python3

### Advent of Code - 2022 - Day 20

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

def mix(orig_input, move_count=1, decrypt_key=1):
    # numbers with their original index and move count
    data = [(n*decrypt_key,i) for i,n in enumerate(orig_input)]

    orig_input = data.copy()
    l = len(data)
    for _ in range(move_count):
        for n in orig_input:
            d = data.index(n)
            i = (d+n[0]) % (l-1)
            data.remove(n)
            data.insert(i,n)
    return data

def get_zero_index(data):
    for i,x in enumerate(data):
        if x[0] == 0:
            return i

start_timer(1)
m = mix(input_nums)
# print(m)
z = get_zero_index(m)
part1(sum([m[(z+o)%len(m)][0] for o in [1000,2000,3000]]))
stop_timer(1)

start_timer(2)
dkey = 811589153
m = mix(input_nums,10,dkey)
# print(m)
z = get_zero_index(m)
part2(sum([m[(z+o)%len(m)][0] for o in [1000,2000,3000]]))
stop_timer(2)