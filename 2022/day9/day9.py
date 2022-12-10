#!/usr/bin/env python3

### Advent of Code - 2022 - Day 9

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

def update_rope(R, dir):
    # Move the Head knot - always
    if dir == 'R':
        R[0][0] += 1
    elif dir == 'D':
        R[0][1] -= 1
    elif dir == 'L':
        R[0][0] -= 1
    else: # 'U'
        R[0][1] += 1

    # Move the rest of the knots
    for r in range(1,len(R)):
        if abs(R[r][0]-R[r-1][0]) <= 1 and abs(R[r][1]-R[r-1][1]) <= 1:
            # The prev knot is within 1 length of the current knot, we can stop
            break
        # We're now more than 1 length from the previous knot
        if R[r-1][0] > R[r][0]:
            # Moving explicitly right
            R[r][0] += 1
            # Check if we need to move diagonally
            if R[r-1][1] > R[r][1]:
                R[r][1] += 1
            elif R[r-1][1] < R[r][1]:
                R[r][1] -= 1
        elif R[r-1][0] < R[r][0]:
            # Moving explicitly left
            R[r][0] -= 1
            # Check if we need to move diagonally
            if R[r-1][1] > R[r][1]:
                R[r][1] += 1
            elif R[r-1][1] < R[r][1]:
                R[r][1] -= 1
        else:
            # Moving explicitly up or down
            if R[r-1][1] > R[r][1]:
                R[r][1] += 1
            else:
                R[r][1] -= 1
    return R

def count_tails(rope):
    tvisited = set()
    tvisited.add(tuple(rope[-1]))
    for m in input_lines:
        tok = m.split()
        dir, amt = tok[0], int(tok[1])
        for _ in range(amt):
            rope = update_rope(rope, dir)
            tvisited.add(tuple(rope[-1]))
    return len(tvisited)

# Part 1
rope = [[0,0] for _ in range(2)]
part1(count_tails(rope))

# Part 2
rope = [[0,0] for _ in range(10)]
part2(count_tails(rope))

