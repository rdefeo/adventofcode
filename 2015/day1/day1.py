#!/usr/bin/env python3

### Advent of Code - 2015 - Day 1

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


def follow_dir(p2=False):
    f = 0
    for i,p in enumerate(finput):
        if p == '(':
            f += 1
        else:
            f -= 1
        if p2 and f == -1:
            return i+1
    return f
part1(follow_dir())
part2(follow_dir(True))

