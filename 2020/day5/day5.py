#!/usr/bin/env python3

### Advent of Code - 2020 - Day 5

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

# take each seat and convert each part to binary. the first 7 bits are the
# row and the last 3 bits are the seat
seatids = []
for b in [l.translate(str.maketrans('FBRL','0110')) for l in input_lines]:
    seatids.append(int(b[0:7],2) * 8 + int(b[7:],2))
part1(f"max seat id = {max(seatids)}")

stop_timer('part 1')

# ###############################
# PART 2
start_timer('part 2')

# we found all seats in part 1, sort them and then look for a case where
# the next seat minus the current seat equals 2 - that means a gap, and
# thus our solution
sids = sorted(seatids)
for s in range(len(sids)-1):
    if sids[s+1]-sids[s] == 2:
        part2(f"my seat id is {sids[s]+1}")

stop_timer('part 2')

#stop_timer()