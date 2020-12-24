#!/usr/bin/env python3

### Advent of Code - 2018 - Day 12

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


# Store our input
pots = collections.defaultdict(lambda:'.')
for i,p in enumerate(input_lines[0].split(' ')[2]):
    pots[i] = p

# handy print method for debugging
def ppots(pots):
    print(''.join([pots[i] for i in range(min(pots),max(pots)+1)]))

# trim left and right of pots. since we default to '.', there's
# no need to have any on the left and right
def trim(pots):
    minp = min(pots)
    while pots[minp] == '.':
        pots.pop(minp)
        minp = min(pots)
    maxp = max(pots)
    while pots[maxp] == '.':
        pots.pop(maxp)
        maxp = max(pots)
    return pots

# read the rules
rules = dict()
for r in input_lines[2:]:
    rules[r.split(' => ')[0]] = r.split(' => ')[1]
# print(rules)

# generate a new set of plants
def generate(pots):
    pots = trim(pots)
    newp = collections.defaultdict(lambda:'.')
    for i in range(min(pots)-4,max(pots)+4):
        llcrr = ''.join([pots[n] for n in range(i,i+5)])
        newp[i+2] = rules[llcrr] if llcrr in rules else '.'
    newp = trim(newp)
    return newp

# print("0: ".rjust(4),end='')
# ppots(pots)

# I noticed that after a few hundred generations, the pattern of
# plants stayed the same, however they continued to shift to the
# right. At that point, no new plants were being generated. Also,
# the score difference between generations stabilized (to 73, for
# my input). A simple calculation yielded the answer for part 2.
old_score = 0
score_diff = 0
for g in range(500):
    pots = generate(pots)
    score = sum([i for i,p in pots.items() if p == '#'])
    if g == 19:
        part1(score)
    score_diff = score-old_score
    old_score = score

plants = sum([i for i,p in pots.items() if p=='#'])
part2((50_000_000_000-500)*score_diff + plants)