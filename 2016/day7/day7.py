#!/usr/bin/env python3

### Advent of Code - 2016 - Day 7

import sys
import requests
import re
import math
import itertools
import functools
import os

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

# TLS requires an ABBA sequence, but only outside of brackets
r_abba = r"(\w)(?!\1)(\w)\2\1"
r_brackets = r"\[[^]]*"+r_abba

valid = 0
for x in input_lines:
    m = re.search(r_abba,x) # find an abba
    if m:
        m = re.search(r_brackets,x) # not one inside a bracket
        if not m:
            valid += 1
part1(valid)

stop_timer('part 1')

# ###############################
# PART 2
start_timer('part 2')

# SSL requires an ABA outside of the brackets, and BAB inside
# rearrange each line so that all outers are on the left, and
# all inners are on the right, of a |
# then just check for the aba...bab match
valid = 0
for x in input_lines:
    inners = re.findall(r"\[(\w+)\]",x)
    for i in inners:
        x = x.replace('['+i+']',' ')
    x = x + '|' + ' '.join(inners)
    if re.search(r".*(\w)(?!\1)(\w)\1.*\|.*\2\1\2.*",x):
        valid += 1
part2(valid)

stop_timer('part 2')

#stop_timer()
