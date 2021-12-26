#!/usr/bin/env python3

### Advent of Code - 2021 - Day 25

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

floor = dict()
for y in range(len(input_lines)):
    for x in range(len(input_lines[0])):
        floor[(x,y)] = input_lines[y][x]
Y = len(input_lines)
X = len(input_lines[0])

def print_floor(f):
    for y in range(Y):
        for x in range(X):
            print(f[(x,y)],end='')
        print('')
    print('')
# print_floor(floor)

def step_east(f):
    nf = dict()
    y = 0
    while y < Y:
        x = 0
        while x < X:
            if f[(x,y)] == '>':
                nx = (x+1) % X
                if f[(nx,y)] == '.':
                    nf[(nx,y)] = '>'
                    nf[(x,y)] = '.'
                    x += 2
                    continue
            nf[(x,y)] = f[(x,y)]
            x += 1
        y += 1
    return nf   

def step_south(f):
    nf = dict()
    x = 0
    while x < X:
        y = 0
        while y < Y:
            if f[(x,y)] == 'v':
                ny = (y+1) % Y
                if f[(x,ny)] == '.':
                    nf[(x,ny)] = 'v'
                    nf[(x,y)] = '.'
                    y += 2
                    continue
            nf[(x,y)] = f[(x,y)]
            y += 1
        x += 1
    return nf

def step(f):
    f = step_east(f)
    f = step_south(f)
    return f

s = 1
while True:
    nf = step(floor)
    if floor == nf:
        part1(s)
        break
    floor = nf
    s += 1
    # print_floor(f)
