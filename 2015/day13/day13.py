#!/usr/bin/env python3

### Advent of Code - 2015 - Day 13

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

# Read the happiness scores and setup score dict
h = dict() # (Person A, Person B) : score
guests = set()
for line in input_lines:
    tok = line.split()
    personA = tok[0]
    personB = tok[-1][:-1] # remove trailing period
    score = int(tok[3]) * (-1 if tok[2] == 'lose' else 1)
    h[(personA,personB)] = score
    guests.add(personA)
    guests.add(personB)

def compute_guest_score(guest_list):
    leng = len(guest_list)
    max_score = 0
    for p in itertools.permutations(guest_list):
        score = 0
        for i in range(leng):
            guest = p[i]
            right = p[(i+1)%leng]
            left = p[(i-1)%leng]
            score += h[(guest, right)]
            score += h[(guest, left)]
        max_score = max(max_score, score)
    return max_score

part1(compute_guest_score(list(guests)))

# Part 2
# Add Yourself as one of the guests, but with a zero score
for g in list(guests):
    h[('Yourself',g)] = 0
    h[(g,'Yourself')] = 0
guests.add('Yourself')
part2(compute_guest_score(list(guests)))
