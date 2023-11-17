#!/usr/bin/env python3

### Advent of Code - 2015 - Day 5

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
    nice = 0
    for s in input_lines:
        vowel = False
        double = False
        valid = False
        if len(re.findall(r"[aeiou]",s)) >= 3:
            vowel = True
        if re.search(r"(\w)\1",s): # letter, match prev
            double = True
        if not any(b in s for b in ['ab','cd','pq','xy']):
            valid = True
        if vowel and double and valid:
            nice += 1
        # print(f"{s.ljust(16)}: {vowel=}, {double=}, {valid=}")
    return nice
part1(solve_p1())

def solve_p2():
    nice = 0
    for s in input_lines:
        pair = False
        between = False
        if len(re.findall(r"(\w\w).*\1",s)): # any 2 letters, anything btw, match prev
            pair = True
        if re.search(r"(\w)\w\1",s): # any letter, any other single letter, match first
            between = True
        if pair and between:
            nice += 1
        # print(f"{s.ljust(16)}: {pair=}, {between=}")
    return nice
part2(solve_p2())