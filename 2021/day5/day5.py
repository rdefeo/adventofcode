#!/usr/bin/env python3

### Advent of Code - 2021 - Day 5

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

def draw_lines(p2 = False):
    vents = collections.defaultdict(int)
    for line in input_lines:
        x1,y1,x2,y2 = list(map(int,re.findall(r'(\d+)',line)))
        if x1 == x2: # vertical line
            for p in range(abs(y2-y1)+1):
                vents[(x1,min(y1,y2)+p)] += 1
            continue
        if y1 == y2: # horizontal line
            for p in range(abs(x2-x1)+1):
                vents[(min(x1,x2)+p,y1)] += 1
            continue
        if p2:
            # diagonal top-left to bottom-right ("back slash")
            if (x1 < x2 and y1 < y2) or (x1 > x2 and y1 > y2):
                for p in range(abs(x2-x1)+1):
                    vents[(min(x1,x2)+p,min(y1,y2)+p)] += 1
            # diagonal bottom-left to top-right ("slash")
            if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
                for p in range(abs(x2-x1)+1):
                    vents[(min(x1,x2)+p,max(y1,y2)-p)] += 1
    return vents

part1(sum([v>=2 for v in draw_lines().values()]))

part2(sum([v>=2 for v in draw_lines(True).values()]))