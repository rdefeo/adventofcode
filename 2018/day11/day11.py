#!/usr/bin/env python3

### Advent of Code - 2018 - Day 11

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
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


def calc_power_level(serial,x,y):
    rackid = x + 10
    power = rackid * y
    power += serial
    power *= rackid
    power = power // 100
    power %= 10
    power -= 5
    return power

# Check calc
assert calc_power_level(8,3,5) == 4
assert calc_power_level(57,122,79) == -5
assert calc_power_level(39,217,196) == 0
assert calc_power_level(71,101,153) == 4



def create_fuel_grid(serial):
    grid = collections.defaultdict(int)
    for y in range(1,301+1):
        for x in range(1,301+1):
            grid[(x,y)] = calc_power_level(serial,x,y)
    return grid

def compute_power(grid,size):
    largest = 0
    largest_coord = (0,0,size)
    for y in range(1,301-size):
        for x in range(1,301-size):
            power = 0
            for r in range(size):
                for c in range(size):
                    power += grid[(x+c,y+r)]
            if power > largest:
                largest = power
                largest_coord = (x,y,size)
    return largest,largest_coord

serial = 8979
# serial = 42

size = 3
grid = create_fuel_grid(serial)
part1(compute_power(grid,size))


grid = create_fuel_grid(serial)
largest = 0
coord = (0,0,size)
for size in range(1,301):
    p,c = compute_power(grid,size)
    if p > largest:
        print("found new largest:",p,c)
        largest = p
        coord = c
part2((largest,coord))