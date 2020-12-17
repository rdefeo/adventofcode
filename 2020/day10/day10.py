#!/usr/bin/env python3

### Advent of Code - 2020 - Day 10

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
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

# Create the full list of adapters, sorted
# add the outlet [0] and your devide (max + 3)
adapters = [0] + sorted(input_nums) + [max(input_nums)+3]
print(adapters)

# compute the diffs between every consecutive adapter
# mutiply the number of 1-diffs and 3-diffs
diffs = [adapters[i+1]-adapters[i] for i in range(len(adapters)-1)]
part1(diffs.count(1)*diffs.count(3))


# for every adapter, see how many we can go to from here
# Since we're recursing, decorate our function with @lru_cache
# to memoize the function! yay!
@lru_cache
def count_links(i):
    if i >= len(adapters)-1:
        return 1
    links = 0
    # from here, i, how many plugs can we go to? count 'em
    for j in range(i+1,i+4): # can jump to at most 3 plugs
        if j < len(adapters) and adapters[j]-adapters[i] <= 3:
            links += count_links(j)
    return links

part2(count_links(0)) # starting at beginning of list

print(count_links.cache_info())

