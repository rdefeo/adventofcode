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

paper = set()
for x,y in [list(map(int,line.split(','))) for line in dots.split()]:
    paper.add((x,y))
X = max(list(map(lambda p: p[0],paper)))
Y = max(list(map(lambda p: p[1],paper)))

for i,f in enumerate(folds.split('\n')):
    dir,fold = f.split()[2].split('=')
    fold = int(fold)

    if dir == 'y': # fold up
        for px,py in [(x,y) for (x,y) in paper if y > fold]:
            paper.add((px,fold-(py-fold)))
            paper.remove((px,py))
        Y = fold
        
    if dir == 'x': # fold left
        for px,py in [(x,y) for (x,y) in paper if x > fold]:
            paper.add((fold-(px-fold),py))
            paper.remove((px,py))
        X = fold

    if i == 0: # Part 1 - num dots after 1 fold
        part1(len(paper))

# Part 2
for y in range(Y):
    for x in range(X):
        print('#',end='') if (x,y) in paper else print(' ',end='')
    print('')