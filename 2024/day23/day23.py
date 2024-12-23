#!/usr/bin/env python3

### Advent of Code - 2024 - Day 23

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

graph = collections.defaultdict(set)
for link in input_lines:
    a,b = link.split('-')
    graph[a].add(b)
    graph[b].add(a)

# Part 1
# Find all groups of 3 computers that are interconnected. We achieve this by 
# finding the intersection of every pair of items that are already known to be
# connected. For every comptuer they share a connection with, that forms a triad.
triads = set()
for c,links in graph.items():
    for l in links:
        i = links & graph[l]
        for ii in i:
            triads.add(tuple(sorted([c,l,ii])))
part1(sum(a[0] == 't' or b[0] == 't' or c[0] == 't' for a,b,c in triads))

# Part 2
# Starting with each computer, try to grow the largest interconnected group
# Before adding a new computer to the group, it must also interconnect to every other
# computer already in that group. Keep track of the largest group found so far.
max_group = set()
for c in graph:
    ng = set()
    ng.add(c)
    for d in graph:
        if all(d in graph[nc] for nc in ng):
            ng.add(d)
    if len(ng) > len(max_group):
        max_group = ng
part2(','.join(sorted(max_group)))