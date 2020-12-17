#!/usr/bin/env python3

### Advent of Code - 2020 - Day 9

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
if len(sys.argv) >= 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

# preamble length
plen = 25
if len(sys.argv) >= 3:
    plen = int(sys.argv[2])

p1 = 0

# find any (x) and (y) in the list (l) where their sum is equal to (n)
def find_sum(l,n):
    for x in l:
        for y in l:
            if x != y and x+y == n:
                return (x,y)
    return False

# Maintain a sliding window of preamble length (plen) elements
# for every element after the sliding window, check if not (find_sum)
# within the preamble
for i in range(len(input_nums)-plen+1):
    pre = input_nums[i:i+plen]
    x = input_nums[i+plen]
    if not find_sum(pre,x):
        p1 = x
        part1(p1)
        break

# for the sum in part 1 (inum), find a continuous list of numbers that
# sum to (inum). once found, sum the min and max of that continuous list
inum = p1
start_timer('part 2')
for i in range(len(input_nums)):
    s = input_nums[i]
    j = i+1
    while j < len(input_nums) and s+input_nums[j] <= inum:
        s += input_nums[j]
        j += 1
    if s == inum and j-1 != i:
        part2(min(input_nums[i:j])+max(input_nums[i:j]))

stop_timer('part 2')
