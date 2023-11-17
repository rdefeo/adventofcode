#!/usr/bin/env python3

### Advent of Code - 2015 - Day 8

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

def decode_hex(h):
    c = h[0][2:]
    if all(x in '0123456789abcdef' for x in c):
        return chr(int(h[0][2:],16))
    return h[0]

def solve_part1():
    literal, memory = 0, 0
    for l in input_lines:
        literal += len(l)
        l = l[1:-1]
        l = l.replace('\\\\','\\',).replace('\\\"','\"')
        l = re.sub(r'\\x(..)',decode_hex,l)
        memory += len(l)
    return literal-memory

part1(solve_part1())

def solve_part2():
    original, encoded = 0, 0
    for l in input_lines:
        original += len(l)
        encoded += len(l) + l.count('\"') + l.count('\\') + 2
    return encoded-original
part2(solve_part2())
