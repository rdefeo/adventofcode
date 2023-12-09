#!/usr/bin/env python3

### Advent of Code - 2023 - Day 8

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

nav, nodes = finput.split('\n\n')
nodes = nodes.split('\n')

# build a dict of 'node' to 0: left, 1: right
net = dict()
for n in nodes:
    names = re.findall(r"\w{3}",n)
    net[names[0]] = (names[1],names[2])

dir = {'L':0,'R':1}

# Part 1
# Simply follow the path from AAA to ZZZ
curr = 'AAA'
steps = 0
for n in itertools.cycle(nav):
    nxt = net[curr][dir[n]]
    steps += 1
    if nxt == 'ZZZ':
        break
    curr = nxt
part1(steps)

# Part 2
# Find all nodes ending in 'A'. For each one, count steps until you reach
# a node ending in 'Z'
anodes = [n for n in net if n[-1] == 'A']
steps = [0 for _ in range(len(anodes))]
for i, curr in enumerate(anodes):
    for n in itertools.cycle(nav):
        nxt = net[curr][dir[n]]
        steps[i] += 1
        if nxt[-1] == 'Z':
            break
        curr = nxt
# Given that we keep cycling through our navigation input, compute the
# Least Common Multiple of all steps to get our answer
part2(math.lcm(*steps))
