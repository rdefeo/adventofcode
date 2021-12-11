#!/usr/bin/env python3

### Advent of Code - 2018 - Day 14

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



def sprint():
    for i,s in enumerate(scores):
        if i == e1:
            print(f"({s})".center(3),end='')
        elif i == e2:
            print(f"[{s}]".center(3),end='')
        else:
            print(f"{s}".center(3),end='')
    print('')

scores = '37'
e1 = 0
e2 = 1
# sprint()
for r in range(200000):
    scores += str(int(scores[e1]) + int(scores[e2]))
    e1 = (e1 + 1 + int(scores[e1])) % len(scores)
    e2 = (e2 + 1 + int(scores[e2])) % len(scores)
# sprint()

r = int(input_lines[0])
part1(scores[r:r+10])

scores = '37'
e1 = 0
e2 = 1
target = input_lines[0]
while target not in scores[-8:]:
    scores += str(int(scores[e1]) + int(scores[e2]))
    e1 = (e1 + 1 + int(scores[e1])) % len(scores)
    e2 = (e2 + 1 + int(scores[e2])) % len(scores)
part2(scores.index(target))
