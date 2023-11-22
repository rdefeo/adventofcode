#!/usr/bin/env python3

### Advent of Code - 2015 - Day 19

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

rep_lines, medicine = finput.split('\n\n')
rep_lines = rep_lines.split('\n')

rep = collections.defaultdict(list)
rrep = dict()
for r in rep_lines:
    a,_,b = r.split()
    rep[a].append(b) # replacements: A => [B, C]
    rrep[b] = a      # reverse replacement: B => A

# For every possible replacement, generate a new molecule and add to set
med_uniq = set()
for k,v in rep.items():
    for m in re.finditer(k,medicine):
        s, e = m.start(0), m.end(0)
        for r in v:
            new_med = medicine[:s] + r + medicine[e:]
            med_uniq.add(new_med)
part1(len(med_uniq))

# Starting with our target molecule, reverse substitute until we can't anymore
# While this works, it's possible that we can dead-end at the wrong solution...
# Did we just get lucky?
count = 0
med = medicine
new_med = ''
while new_med != med:
    new_med = med
    for k,v in rrep.items():
        while k in med:
            count += med.count(k)
            med = med.replace(k,v)
part2(count)
    
