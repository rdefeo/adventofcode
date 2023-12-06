#!/usr/bin/env python3

### Advent of Code - 2023 - Day 4

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

total_score = 0
copies = [1 for _ in range(len(input_lines))]
for c, card in enumerate(input_lines):
    winning, have = card.split('|')
    card_no, winning = winning.split(':')
    card_no = int(card_no.split()[1].strip())
    winning = list(map(int,winning.split()))
    have = list(map(int,have.split()))
    # print(card_no, winning, have)

    matches = sum(h in winning for h in have)
    score = 2**max(matches-1,0) if matches else 0
    # print(f"{card_no=} : {matches=}, {score=}")

    total_score += score
    for m in range(matches):
        copies[c+1+m] += copies[c]

part1(total_score)
part2(sum(copies))
