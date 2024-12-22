#!/usr/bin/env python3

### Advent of Code - 2024 - Day 21

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

codes = input_lines

# How to get from one key to another on the numeric keypad
numeric_kp_path = {
    'A': { 'A': 'A', '0': '<A', '1': '^<<A', '2': '<^A', '3': '^A', '4': '^^<<A', '5': '<^^A', '6': '^^A', '7': '^^^<<A', '8': '<^^^A', '9': '^^^A' },
    '0': { 'A': '>A', '0': 'A', '1': '^<A', '2': '^A', '3': '^>A', '4': '^^<A', '5': '^^A', '6': '^^>A', '7': '^^^<A', '8': '^^^A', '9': '^^^>A' },
    '1': { 'A': '>>vA', '0': '>vA', '1': 'A', '2': '>A', '3': '>>A', '4': '^A', '5': '^>A', '6': '^>>A', '7': '^^A', '8': '^^>A', '9': '^^>>A' },
    '2': { 'A': '>vA', '0': 'vA', '1': '<A', '2': 'A', '3': '>A', '4': '^<A', '5': '^A', '6': '^>A', '7': '^^<A', '8': '^^A', '9': '^^>A' },
    '3': { 'A': 'vA', '0': '<vA', '1': '<<A', '2': '<A', '3': 'A', '4': '<<^A', '5': '<^A', '6': '^A', '7': '<<^^A', '8': '<^^A', '9': '^^A' },
    '4': { 'A': '>>vvA', '0': '>vvA', '1': 'vA', '2': '>vA', '3': '>>vA', '4': 'A', '5': '>A', '6': '>>A', '7': '^A', '8': '^>A', '9': '^>>A' },
    '5': { 'A': 'vv>A', '0': 'vvA', '1': 'v<A', '2': 'vA', '3': 'v>A', '4': '<A', '5': 'A', '6': '>A', '7': '<^A', '8': '^A', '9': '^>A' },
    '6': { 'A': 'vvA', '0': 'vv<A', '1': 'v<<A', '2': 'v<A', '3': 'vA', '4': '<<A', '5': '<A', '6': 'A', '7': '<<^A', '8': '<^A', '9': '^A' },
    '7': { 'A': '>>vvvA', '0': '>vvvA', '1': 'vvA', '2': '>vvA', '3': '>>vvA', '4': 'vA', '5': '>vA', '6': '>>vA', '7': 'A', '8': '>A', '9': '>>A' },
    '8': { 'A': 'vvv>A', '0': 'vvvA', '1': 'vv<A', '2': 'vvA', '3': '>vvA', '4': 'v<A', '5': 'vA', '6': '>vA', '7': '<A', '8': 'A', '9': '>A' },
    '9': { 'A': 'vvvA', '0': 'vvv<A', '1': 'vv<<A', '2': 'vv<A', '3': 'vvA', '4': 'v<<A', '5': 'v<A', '6': 'vA', '7': '<<A', '8': '<A', '9': 'A' }
}

# How to get from one key to another on the direction keypad
direction_kp_path = {
    'A': { 'A': 'A', '^': '<A', '>': 'vA', '<': 'v<<A', 'v': '<vA' },
    '^': { 'A': '>A', '^': 'A', '>': 'v>A', '<': 'v<A', 'v': 'vA' },
    '>': { 'A': '^A', '^': '<^A', '>': 'A', '<': '<<A', 'v': '<A' },
    '<': { 'A': '>>^A', '^': '>^A', '>': '>>A', '<': 'A', 'v': '>A' },
    'v': { 'A': '^>A', '^': '^A', '<': '<A', '>': '>A', 'v': 'A' }
}

def gen_numeric_keys(code):
    seq = []
    curr = 'A'
    for n in code:
        seq.append(numeric_kp_path[curr][n])
        curr = n
    return ''.join(seq)

def gen_direction_keys(code):
    seq = []
    curr = 'A'
    for n in code:
        seq.append(direction_kp_path[curr][n])
        curr = n
    return ''.join(seq)

# Part 1
# Simply brute force the direction key expansion with two robots
total_complexity = 0
for code in codes:
    nk = gen_numeric_keys(code)
    nk = gen_direction_keys(nk)
    nk = gen_direction_keys(nk)
    total_complexity += len(nk) * int(code[:-1])
part1(total_complexity)

# Part 2
# Split the numeric expansion into instructions that end in 'A'
# (Pressing 'A' resets the robot's position, so all instructions are independent)
# Then, count the instructions
# For each loop iteration, create a count of the next generated instructions
# Multiply the counts of the new instructions by the count of the originating instruction
# Loop
total_complexity = 0
for code in codes:
    nk = gen_numeric_keys(code)    
    instructions = collections.Counter([c+'A' for c in nk.split('A')[:-1]])
    
    for _ in range(25):
        new_insts = collections.Counter()
        for inst,cnt in instructions.items():
            new_inst = gen_direction_keys(inst)
            tinsts = collections.Counter([c+'A' for c in new_inst.split('A')[:-1]])
            for t in tinsts:
                new_insts[t] += tinsts[t] * cnt
        instructions = new_insts

    total_complexity += sum(len(i)*c for i,c in instructions.items()) * int(code[:-1])
part2(total_complexity)
