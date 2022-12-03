#!/usr/bin/env python3

### Advent of Code - 2022 - Day 3

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

# Part 1
s = 0
for rucksack in input_lines:
    l = len(rucksack)
    a, b = set(rucksack[:l//2]), set(rucksack[l//2:])
    i = a.intersection(b)
    b = list(i)[0]
    print(b)
    if b.islower():
        p = 1 + ord(b)-ord('a')
    else:
        p = 27 + ord(b)-ord('A')
    print(p)
    s += p
part1(s)

# Part 2
s = 0
for r in range(0,len(input_lines),3):
    a, b, c = input_lines[r], input_lines[r+1], input_lines[r+2]
    a, b, c = set(a), set(b), set(c)
    i = a.intersection(b).intersection(c)
    b = list(i)[0]
    if b.islower():
        p = 1 + ord(b)-ord('a')
    else:
        p = 27 + ord(b)-ord('A')
    s += p
part2(s)