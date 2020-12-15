#!/usr/bin/env python3

### Advent of Code - 2020 - Day 15

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
#input_lines = [line.strip() for line in input.split('\n')]
#input_nums = list(map(int,input_lines))
#print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

nums = list(map(int,input.split(',')))

print(nums)

def speak_numbers(nums,turns):
    spoken = dict()
    for i, n in enumerate(nums):
        spoken[n] = i+1
    last_spoken = nums[-1]
    for turn in range(len(nums),turns):
        if last_spoken not in spoken:
            spoken[last_spoken] = turn
            last_spoken = 0
        else:
            when = spoken[last_spoken]
            spoken[last_spoken] = turn
            last_spoken = turn - when
    return(last_spoken)

start_timer('part 1')
part1(speak_numbers(nums,2020))
stop_timer('part 1')

start_timer('part 2')
part2(speak_numbers(nums,30000000))
stop_timer('part 2')
