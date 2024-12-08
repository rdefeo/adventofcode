#!/usr/bin/env python3

### Advent of Code - 2024 - Day 8

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

p2a = collections.defaultdict(lambda:'')
a2p = collections.defaultdict(list)
for y, line in enumerate(input_lines):
    for x, a in enumerate(line):
        p2a[(x,y)] = a
        if a != '.':
            a2p[a].append((x,y))

def count_antinodes(p2=False):
    antinodes = set()
    for _,pos in a2p.items():
        if p2: # in Part 2, existing locations count
            antinodes.update(pos)

        for i,p in enumerate(pos):
            for j in range(i+1,len(pos)):
                dx, dy = pos[j][0]-p[0], pos[j][1]-p[1]

                # check on direction
                np = (p[0]-dx, p[1]-dy)
                while p2a[np] != '':
                    antinodes.add(np)
                    if not p2: break
                    np = (np[0]-dx, np[1]-dy)

                # now the other direction
                np = (pos[j][0]+dx, pos[j][1]+dy)
                while p2a[np] != '':
                    antinodes.add(np)
                    if not p2: break
                    np = (np[0]+dx, np[1]+dy)
    return len(antinodes)

part1(count_antinodes())
part2(count_antinodes(True))


