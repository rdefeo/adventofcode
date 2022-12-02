#!/usr/bin/env python3

### Advent of Code - 2022 - Day 2

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


# points for each choice
A, B, C = 1, 2, 3 # rock, paper, scissors
X, Y, Z = 1, 2, 3 # rock, paper, scissors
W, L, D = 6, 0, 3

# Part 1 - original
total = 0
for h in input_lines:
    o, m = h.split()
    s = 0
    s += eval(m)
    # I win
    if (m == 'Z' and o == 'B') or (m == 'Y' and o == 'A') or (m == 'X' and o == 'C'):
        s += W
    # I lose
    elif (o == 'A' and m == 'Z') or (o == 'B' and m == 'X') or (o == 'C' and m == 'Y'):
        s += L
    # I draw
    else:
        s += D
    # print(s)
    total += s
part1(total)

# Part 1 - rewritten
points = {
    # there are only 9 possible combinations!
    'A Y': 6, 'B Z': 6, 'C X': 6, # win
    'A X': 3, 'B Y': 3, 'C Z': 3, # draw
    'A Z': 0, 'B X': 0, 'C Y': 0, # lose
    }
total = 0
for h in input_lines:
    total += eval(h.split()[1]) + points[h]
part1(total)

# Part 2 - original
total = 0
for h in input_lines:
    o, r = h.split()
    s = 0
    # I win
    if (r == 'Z'):
        s += W
        if o == 'A':
            m = 'Y'
        elif o == 'B':
            m = 'Z'
        else:
            m = 'X'
    # I lose
    if (r == 'X'):
        s += L
        if o == 'A':
            m = 'Z'
        elif o == 'B':
            m = 'X'
        else:
            m = 'Y'
    # I draw
    if (r == 'Y'):
        s += D
        if o == 'A':
            m = 'X'
        elif o == 'B':
            m = 'Y'
        else:
            m = 'Z'
    s += eval(m)
    # print(s)
    total += s
part2(total)

# Part 2 - rewritten
points = { 'X': 0, 'Y': 3, 'Z': 6 } # points for each result
strategy = {
    # for each result, what must I play against the opponent?
    'X': {'A': Z, 'B': X, 'C': Y}, # lose
    'Y': {'A': X, 'B': Y, 'C': Z}, # draw
    'Z': {'A': Y, 'B': Z, 'C': X}, # win
    }
total = 0
for h in input_lines:
    opp, res = h.split()
    total += strategy[res][opp] + points[res]
part2(total)
