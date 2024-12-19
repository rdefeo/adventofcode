#!/usr/bin/env python3

### Advent of Code - 2024 - Day 19

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

patterns, designs = finput.split("\n\n")
patterns, designs = patterns.split(", "), designs.split("\n")

# Part 1
# Build a single regex of all patterns and let re do it's thing
matches = 0
for design in designs:
    m = re.match(r"^(" + "|".join(patterns) + ")+$", design)
    if m:
        matches += 1
part1(matches)

# Part 2
# Recursively pull off the beginning of the design if it matches a pattern
# If we're able to consume the design entirely, then we've found one possible
# arrangement, return 1
# Caching makes things run faster
@lru_cache
def count_patterns(design):
    if len(design) == 0:
        return 1
    counts = 0
    for pattern in patterns:
        if design.startswith(pattern):
            counts += count_patterns(design[len(pattern):])
    return counts

part2(sum(count_patterns(design) for design in designs))
