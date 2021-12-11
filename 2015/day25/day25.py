#!/usr/bin/env python3

### Advent of Code - 2015 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
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

# Enter the code at row 2947, column 3029.

row = 2947
col = 3029

n = 20151125
i = 1
x = y = 1
while True:
    if y == 1:
        y = x + 1
        x = 1
    else:
        y -= 1
        x += 1
    n = (n * 252533) % 33554393
    i += 1
    if y == row and x == col:
        part1(n)
        break

def mod_pow(base,exp,modulus):
    if modulus == 1:
        return 0
    c = 1
    for ep in range(exp):
        c = (c * base) % modulus
    return c    
    
part1( (20151125 * mod_pow(252533,i,33554393)) % 33554393)


