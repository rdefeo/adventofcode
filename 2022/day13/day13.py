#!/usr/bin/env python3

### Advent of Code - 2022 - Day 13

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

# -1 : l < r, we're in order
#  0 : equal
#  1 : greater than
def packet_compare(l, r):
    # print(f"checking {l} and {r}")
    if l is None:
        return -1
    if r is None:
        return 1
    if type(l) == type(r) == int:
        if l < r:
            return -1
        elif l > r:
            return 1
        return 0
    if type(l) == int and type(r) == list:
        return packet_compare([l],r)
    elif type(l) == list and type(r) == int:
        return packet_compare(l,[r])
    else: # both are lists
        for x, y in itertools.zip_longest(l, r):
            c = packet_compare(x,y)
            if c == 0: continue
            return c
        return 0

# Part 1
results = []
for i,p in enumerate(finput.split('\n\n')):
    l, r = p.split('\n')
    c = packet_compare(eval(l),eval(r))
    # print(i+1,l,r,o)
    results.append(c)
print(results)
part1(sum(i+1 for i,r in enumerate(results) if r < 0))

# Part 2
all_packets = [ [[2]], [[6]] ]
for i,p in enumerate(finput.split('\n\n')):
    l, r = p.split('\n')
    all_packets.append(eval(l))
    all_packets.append(eval(r))
sorted_packets = sorted(all_packets,key=functools.cmp_to_key(packet_compare))
# print(sorted_packets)
part2((sorted_packets.index([[2]])+1) * (sorted_packets.index([[6]])+1))

