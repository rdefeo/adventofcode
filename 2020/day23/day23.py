#!/usr/bin/env python3

### Advent of Code - 2020 - Day 23

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
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

# Part 1
# Simple approach using list splicing. Works well for Part 1!
# I keep the 'current' cup at the head of the list to avoid having
# to split my pickup insertion across the end and beginning of
# the list

cups = list(map(int,input))
#cups = list(map(int,'389125467')) # sample

max_cup = max(cups)
min_cup = min(cups)

for _ in range(100):
    label = cups[0] - 1
    
    # pickup 3 cups - check for wraparound
    pickup = cups[1:4]
    cups = cups[0:1]+cups[4:]
    
    while label < min_cup or label in pickup:
        label -= 1
        if label < min_cup:
            label = max_cup

    ilabel = 0
    for i,l in enumerate(cups):
        if l == label:
            ilabel = i
            break
    cups = cups[:ilabel+1] + pickup + cups[ilabel+1:]
    cups = cups[1:]+cups[:1] # shift list left one (i.e. move 'current' forward)

# prints the entire list, including the 1, just copy paste to get the
# digits following the 1 in the correct order
part1(''.join(list(map(str,cups))))


# Part 2
# Simple list splicing was incredibly slow. Instead, use a combinaiton of
# a singly-linked list (for fast list splicing, no copies) and a dictionary
# to quickly find the locations of nodes (versus linear searching)

class Cup:
    def __init__(self,num):
        self.num = num
        self.next = None
    def __repr__(self):
        return str(self.num)

cups = list(map(int,input))
#cups = list(map(int,'389125467')) # sample

for x in range(10,1000000+1):
    cups.append(x)

max_cup = max(cups)
min_cup = min(cups)

all_cups = {}  # dict[ cup value ] => Cup node
prev_cup = None
for c in cups:
    all_cups[c] = Cup(c)
    if prev_cup:
        all_cups[prev_cup].next = all_cups[c]
    prev_cup = c
all_cups[cups[-1]].next = all_cups[cups[0]] # link the last cup to the first

current = all_cups[cups[0]]
for move in range(10000000):
    p1 = current.next
    p2 = p1.next
    p3 = p2.next
     
    dest = current.num - 1
    while dest < min_cup or dest in [p1.num,p2.num,p3.num]:
        dest -= 1
        if dest < min_cup:
            dest = max_cup
    
    left = all_cups[dest]
    right = left.next

    current.next = p3.next
    left.next = p1
    p3.next = right
    current = current.next

cup1 = all_cups[1]
part2(cup1.next.num * cup1.next.next.num)