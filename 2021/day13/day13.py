#!/usr/bin/env python3

### Advent of Code - 2021 - Day 13

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

dots, folds = finput.split('\n\n') # two lists in input

paper = set(tuple(map(int,line.split(','))) for line in dots.split())

for i,f in enumerate(folds.split('\n')):
    dir,fold = f.split()[2].split('=')
    fold = int(fold)

    if dir == 'y': # fold up
        paper = set((x,y) if y < fold else (x,fold-(y-fold)) for x,y in paper)
    if dir == 'x': # fold left
        paper = set((x,y) if x < fold else (fold-(x-fold),y) for x,y in paper)

    if i == 0: # Part 1 - num dots after 1 fold
        part1(len(paper))

# Part 2
for y in range(max(list(map(lambda p: p[1]+1,paper)))):
    for x in range(max(list(map(lambda p: p[0]+1,paper)))):
        print('#',end='') if (x,y) in paper else print(' ',end='')
    print('')