#!/usr/bin/env python3

### Advent of Code - 2018 - Day 1

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

freq = 0
for x in input_lines:
    n = int(x)
    freq += n
part1(freq)

freq = 0
fseen = set()
while freq not in fseen:
    for x in input_lines:
        fseen.add(freq)
        n = int(x)
        freq += n
        if freq in fseen:
            part2(freq)
            quit()
