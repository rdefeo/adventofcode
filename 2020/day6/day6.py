#!/usr/bin/env python3

### Advent of Code - 2020 - Day 6

import sys
import requests
import re
import math
import itertools
import functools
import os

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, length: {len(input_lines)}"+CLEAR)

#start_timer()

# ###############################
# PART 1
start_timer('part 1')

counts = 0
for g in input.rstrip().split("\n\n"):
    qs = set()
    for line in [x.strip() for x in g]:
        for q in line:
            qs.add(q)
    counts += len(qs)

part1(counts)

stop_timer('part 1')

# ###############################
# PART 2
start_timer('part 2')

counts = 0
groups = input.rstrip().split("\n\n")
for g in [grp.split("\n") for grp in groups]:
    qs = dict()
    for line in g:
        for q in line:
            if q not in qs:
                qs[q] = 1
            else:
                qs[q] += 1
    c = 0
    for q in qs:
        if qs[q] == len(g):
            c += 1
    counts += c

part2(counts)

stop_timer('part 2')

#stop_timer()
