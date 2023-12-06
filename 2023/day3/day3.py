#!/usr/bin/env python3

### Advent of Code - 2023 - Day 3

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

gears = collections.defaultdict(list)

def near_symbol(x1, x2, y):
    """ For a given number on row y, between x1 and x2, check the
    surrounding spaces for a symbol. Return the symbol and it's position """
    # Check the row above us, one space wider on each side
    for x in range(x1-1,x2+1):
        if smatic[y-1][x] not in '.0123456789':
            return smatic[y-1][x], (x,y-1)
    # Check immediate left
    if smatic[y][x1-1] not in '.0123456789':
        return smatic[y][x1-1], (x1-1,y)
    # Check immediate right
    if smatic[y][x2] not in '.0123456789':
        return smatic[y][x2], (x2,y)
    # Check row below us
    for x in range(x1-1,x2+1):
        if smatic[y+1][x] not in '.0123456789':
            return smatic[y+1][x], (x,y+1)
    return None, (0,0)

# Pad our input schematic with a '.' border to make edge cases simpler
smatic = ['.' * (len(input_lines[0]) + 2)]
smatic += ['.'+line+'.' for line in input_lines]
smatic += ['.' * (len(input_lines[0]) + 2)]

parts_sum = 0
for y in range(len(smatic)):
    num_start = -1
    print(y,': ',end='')
    for x in range(len(smatic[y])):
        if smatic[y][x] in '0123456789':
            if num_start < 0:
                num_start = x
        elif num_start >= 0:
            num = int(smatic[y][num_start:x])
            sym, pos = near_symbol(num_start, x, y)
            if sym:
                parts_sum += num
                # print(y, num, near)
                print(num,' ',pos,' ',end='')
                if sym == '*':
                    gears[pos].append(num)
            num_start = -1
    print()

part1(parts_sum)

part2(sum(v[0]*v[1] for v in gears.values() if len(v) == 2))