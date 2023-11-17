#!/usr/bin/env python3

### Advent of Code - 2015 - Day 10

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


def say(s):
    prev_d = s[0]
    c = 0
    res = ''
    for d in s:
        if d == prev_d:
            c += 1
        else:
            res += str(c) + prev_d
            c = 1
            prev_d = d
    return res + str(c) + prev_d

print(say('1'))
print(say('11'))
print(say('21'))
print(say('1211'))
print(say('111221'))
# exit()
s = finput
for _ in range(40):
    s = say(s)
part1(len(s))

s = finput
for _ in range(50):
    s = say(s)
part2(len(s))


