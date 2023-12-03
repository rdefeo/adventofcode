#!/usr/bin/env python3

### Advent of Code - 2023 - Day 1

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
#input_nums = list(map(int,input_lines))

# Part 1
val = 0
for line in input_lines:
    m = re.findall(r"\d",line)
    if m:
        # print(m[0],m[-1])
        val += int(str(m[0])+str(m[-1]))
part1(val)

# Part 2
nums = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}
val = 0
for line in input_lines:
    # This only works for our first 'digit' since regex matches are non-overlapping
    # Some digits overlap: for '...eightwo', our last match would be 'eight' and not 'two'
    m = re.findall(r"\d|one|two|three|four|five|six|seven|eight|nine",line)
    n1, n2 = 0, 0
    if m:
        n1 = nums[m[0]] if m[0] in nums else int(m[0])
    # To find the last digit, we walk backwards, looking at more and more characters
    # until we find a digit. Not elegant, but it works.
    for i in range(len(line)-1,-1,-1):
        m = re.findall(r"\d|one|two|three|four|five|six|seven|eight|nine",line[i:])
        if m:
            n2 = nums[m[-1]] if m[-1] in nums else int(m[-1])
            break

    #print(n1,n2, n1*10+n2, line)
    val += n1*10 + n2
part2(val)
