#!/usr/bin/env python3

### Advent of Code - 2019 - Day 6

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

orbits = dict()
for line in input_lines:
    a,b = line.split(')')
    orbits[b] = a

# Compute the full path from each satellite to COM, as a list
def path_to_COM(sat):
    path = []
    while sat != 'COM':
        path.append(sat)
        sat = orbits[sat]
    return path

# Part 1
# Simply sum the length of every path to COM for every object
part1(sum(len(path_to_COM(s)) for s in orbits))

# Part 2
# Get the path to COM for YOu and SAN
# Calc the number of objects that are mutually exclusive between the paths
YOU = set(path_to_COM(orbits['YOU']))
SAN = set(path_to_COM(orbits['SAN']))
part2(len(YOU^SAN))
