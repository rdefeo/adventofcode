#!/usr/bin/env python3

### Advent of Code - 2021 - Day 14

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from collections import Counter

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

polymer, maps = finput.split('\n\n')
pairs = dict()
for m in maps.split('\n'):
    a,b = m.split(' -> ')
    pairs[a] = b

# Part 1

# for each pair, create a new polymer with the inserted element
def insert(polymer):
    pout = ''
    for p in [polymer[x:x+2] for x in range(len(polymer)-1)]:
        if p in pairs:
            pout += p[0]+pairs[p]
    return pout+polymer[-1]

res = polymer
for _ in range(10):
    res = insert(res)
elems = Counter(res)
part1(elems.most_common()[0][1]-elems.most_common()[-1][1])


# Part 2
# algo from above won't work....
# every pair creates two new pairs, we don't need to create a full string

pcount = Counter()
# count the pairs in the input
for p in [polymer[i:i+2] for i in range(len(polymer)-1)]:
    pcount[p] += 1

for _ in range(40):
    npcount = Counter()
    # for each pair, create the new left and right pair and count them, repeat
    for p,c in pcount.items():
        m = pairs[p]
        lpair, rpair = p[0]+m, m+p[1]
        npcount[lpair] += c
        npcount[rpair] += c
    pcount = npcount

# for each of the pairs, count the individual elements
elems = Counter()
for pair,c in pcount.items():
    elems[pair[0]] += c
    elems[pair[1]] += c
# the elements in every pair are double counted, except the first and last element, add them
elems[polymer[0]] += 1
elems[polymer[-1]] += 1
# divide the most-least by 2
part2((elems.most_common()[0][1]-elems.most_common()[-1][1]) // 2)
