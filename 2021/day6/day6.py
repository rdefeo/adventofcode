#!/usr/bin/env python3

### Advent of Code - 2021 - Day 6

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from collections import Counter

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

fish = [int(l) for l in finput.split(',')]

def spawn_count(fish,days):
    for _ in range(days):
        newfish = Counter()
        for k,v in fish.items():
            if k == 0:
                newfish[6] += v
                newfish[8] += v
            else:
                newfish[k-1] += v
        fish = newfish
    return sum(fish.values())

part1(spawn_count(Counter(fish),80))
part2(spawn_count(Counter(fish),256))

