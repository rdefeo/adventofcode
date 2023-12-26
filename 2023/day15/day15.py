#!/usr/bin/env python3

### Advent of Code - 2023 - Day 15

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


def gen_hash(string):
    n = 0
    for c in string:
        n += ord(c)
        n *= 17
        n %= 256
    return n

print(gen_hash('HASH'))

init_seq = 0
for step in finput.split(','):
    h = gen_hash(step)
    init_seq += h
part1(init_seq)

boxes = [[] for _ in range(256)]
for step in finput.split(','):
    flen = None
    if step[-1].isdigit():
        flen = int(step[-1])
        step = step[:-1]
    op = step[-1]
    label = step[:-1]
    box = gen_hash(label)
    if op == '-':
        for bi in range(len(boxes[box])):
            if boxes[box][bi][0] == label:
                del boxes[box][bi]
                break
    else:
        found = False
        for bi in range(len(boxes[box])):
            if boxes[box][bi][0] == label:
                found = True
                boxes[box][bi] = (label,flen)
        if not found:
            boxes[box].append((label,flen))
    # print(boxes[:10])

power = 0
for b, box in enumerate(boxes):
    for s, lens in enumerate(box):
        power += (b+1) * (s+1) * lens[1]
part2(power)

