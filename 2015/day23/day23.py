#!/usr/bin/env python3

### Advent of Code - 2015 - Day 23

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

A = 1 # part1, A=0
B = 0

pc = 0
while 0 <= pc < len(input_lines):
    tokens = input_lines[pc].split(' ')
    print(A,B,tokens)
    op = tokens[0]
    if op == 'hlf':
        if tokens[1] == 'a':
            A //= 2
        else:
            B //= 2
        pc += 1
    elif op == 'tpl':
        if tokens[1] == 'a':
            A *= 3
        else:
            B *= 3
        pc += 1
    elif op == 'inc':
        if tokens[1] == 'a':
            A += 1
        else:
            B += 1
        pc += 1
    elif op == 'jmp':
        pc += int(tokens[1])
    elif op == 'jie':
        if tokens[1][0] == 'a':
            pc += int(tokens[2]) if A%2==0 else 1
        else:
            pc += int(tokens[2]) if B%2==0 else 1
    elif op == 'jio':
        if tokens[1][0] == 'a':
            pc += int(tokens[2]) if A==1 else 1
        else:
            pc += int(tokens[2]) if B==1 else 1
part1(f"A = {A}, B = {B}")
