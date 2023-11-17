#!/usr/bin/env python3

### Advent of Code - 2015 - Day 2

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

def solve_p1():
    sf = 0
    for b in input_lines:
        w,l,h = sorted(map(int,b.split('x')))
        sf += 2*w*l + 2*w*h + 2*l*h + w*l
    return sf

def solve_p2():
    rl = 0
    for b in input_lines:
        w,l,h = sorted(map(int,b.split('x')))
        rl += 2*w + 2*l + w*l*h
    return rl

part1(solve_p1())
part2(solve_p2())
