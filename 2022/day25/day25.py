#!/usr/bin/env python3

### Advent of Code - 2022 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import operator

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

def snafu_to_dec(s: str):
    value = { '2':2, '1':1, '0':0, '-':-1, '=':-2 }
    snafu = 0
    for i,d in enumerate(s[::-1]):
        snafu += value[d] * math.pow(5,i)
    return int(snafu)

def dec_to_snafu(d):
    snafu = ''
    while d:
        d, r = divmod(d, 5)
        snafu += '012=-'[r]
        if r >= 3:
            d += 1
    return snafu[::-1]

part1(dec_to_snafu(sum([snafu_to_dec(line) for line in input_lines])))
