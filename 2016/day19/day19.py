#!/usr/bin/env python3

### Advent of Code - 2016 - Day 19

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

class Elf:
    def __init__(self,id):
        self.id = id
        self.p = 1
        self.next = None
    def __repr__(self):
        return f"{self.p}"

max_presents = 3017957 # 5
elves = [Elf(e+1) for e in range(max_presents)]
prev_elf = None
for e in elves:
    if prev_elf:
        prev_elf.next = e
    prev_elf = e
elves[-1].next = elves[0]

part_1 = False
while part_1:
    for e in elves:
        if e.p:
            n = e.next
            while not n.p:
                n = n.next
            e.p += n.p
            n.p = 0
            if e.p == max_presents:
                part1(f"Elf {e.id} has {e.p} presents")
                quit()

if not part_1:
    p = 1
    while 3 * p < max_presents:
        p *= 3
    if max_presents <= 2 * p:
        part2(max_presents-p)
        quit()
    r = max_presents % p
    if r == 0:
        r = p
    part2(max_presents-p+r)
    quit()
print("next solution")


# if not part_1:
#     elves = collections.deque(range(1,max_presents+1))
#     eleft = len(elves)
#     elves.rotate(-(eleft // 2))
#     while eleft > 1:
#         if eleft & 1 == 0:
#             elves.rotate(-1)
#         elves.popleft()
#         eleft -= 1
#     part2(elves.popleft())