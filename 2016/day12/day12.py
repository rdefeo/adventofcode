#!/usr/bin/env python3

### Advent of Code - 2016 - Day 12

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

R = [0,0,1,0] #part1: c = 0, part2: c = 1

pc = 0
while 0 <= pc < len(input_lines):
    tokens = input_lines[pc].split(' ')
    # print(R,tokens)
    if tokens[0] == 'cpy':
        val = 0
        if tokens[1].isalpha():
            val = R[ord(tokens[1])-ord('a')]
        else:
            val = int(tokens[1])
        R[ord(tokens[2])-ord('a')] = val
        pc += 1
    elif tokens[0] == 'inc':
        R[ord(tokens[1])-ord('a')] += 1
        pc += 1
    elif tokens[0] == 'dec':
        R[ord(tokens[1])-ord('a')] -= 1
        pc += 1
    elif tokens[0] == 'jnz':
        if tokens[1].isalpha():
            if R[ord(tokens[1])-ord('a')] != 0:
                pc += int(tokens[2])
            else:
                pc += 1
        else:
            if int(tokens[1]) != 0:
                pc += int(tokens[2])
            else:
                pc += 1
    else:
        print("Unknown instruction!")
print(R)