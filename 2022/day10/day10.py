#!/usr/bin/env python3

### Advent of Code - 2022 - Day 10

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

X = 1
cycles = 0
strength = dict()
CRT = ['.' for _ in range(40*6)]

def update_cycle():
    global cycles
    global strength
    global CRT
    cycles += 1
    if cycles == 20:
        print(f"{cycles} : {X}")
        strength[cycles] = cycles * X
    elif (cycles-20)%40 == 0:
        print(f"{cycles} : {X}")
        strength[cycles] = cycles * X
    if X-1 <= (cycles-1)%40 <= X+1:
        CRT[cycles-1] = '#'

for op in input_lines:
    update_cycle()
    if op == 'noop':
        continue
    elif op.startswith('addx'):
        amt = int(op.split()[1])
        update_cycle()
        X += amt

part1(sum(strength.values()))

for r in range(6):
    print(''.join(CRT[r*40:r*40+40]))