#!/usr/bin/env python3

import sys
import requests
import re
import math
import itertools
import functools

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as array
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
input = open(inputfile,'r').readlines()

start_timer()

# PART 1
start_timer('part 1')

# simply count the number of times the letter (m.group(3)) occurs
# in the password (m.group(4)) and if it's in the range of
# [m.group(1),m.group(2)+1], then it's valid
valid = 0
for p in input:
    m = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)",p)
    if m:
        s = m.group(4).count(m.group(3))
        if s in range(int(m.group(1)),int(m.group(2))+1):
            valid += 1
part1(valid)
stop_timer('part 1')

# PART 2
start_timer('part 2')

# Similar to the above, but instead verify if the letter (m.group(3))
# is in one of the positions (m.group(1)) or (m.group(2))
valid = 0
for p in input:
    m = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)",p)
    if m:
        a = m.group(4)[int(m.group(1))-1]
        b = m.group(4)[int(m.group(2))-1]
        c = m.group(3)
        if (a == c and b != c) or (a != c and b == c):
            valid += 1

part2(valid)


stop_timer('part 2')

stop_timer()