#!/usr/bin/env python3

### Advent of Code - 2021 - Day 3

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from collections import Counter

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
# input_nums = list(map(int,input_lines))

# PART 1

gamma, epsilon = '', ''
# create list of all first digits, then all second digits, etc
# count the occurrences of each bit: Counter('11010') = {'1':3, '0':2}
for b in [Counter(x) for x in list(zip(*input_lines))]:
    gamma += max(b,key=b.get)   # get the key/bit with the highest count
    epsilon += min(b,key=b.get) # ... and the lowest count
print(f"{gamma=}, {epsilon=}")
part1(int(gamma,2)*int(epsilon,2))

# PART 2

# finds the most/least common bit for position p
# for every p, build up the resulting value in val
# filter the list of lines, repeat
def get_bit_value(lines,func):
    val = ''
    val_lines = lines
    for p in range(len(lines[0])):
        trans = list(zip(*val_lines))
        c = Counter(trans[p])
        if c['1'] == c['0']: # tie breaker
            val += str(func(1,0)) 
        else:
            val += func(c,key=c.get)
       
        new_lines = [line for line in val_lines if line[p] == val[p]]
        if len(new_lines) == 1:
            val = new_lines[0]
            break
        val_lines = new_lines
    return val

oxy = get_bit_value(input_lines,max)
co2 = get_bit_value(input_lines,min)
print(f"{oxy=}, {co2=}")
part2(int(oxy,2)*int(co2,2))

