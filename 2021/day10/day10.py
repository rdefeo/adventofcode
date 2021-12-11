#!/usr/bin/env python3

### Advent of Code - 2021 - Day 10

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

score_p1 = 0
scores_p2 = []
for l in input_lines:
    # keep trying to eliminate zero chunks
    ol, nl = '', l
    while ol != nl: 
        ol = nl
        nl = nl.replace('()','').replace('[]','').replace('{}','').replace('<>','')
    
    # check for syntax_errors
    syntax_error = False
    for c in nl:
        if c in ')]}>':
            score_p1 += { ')': 3, ']': 57, '}': 1197, '>': 25137 }[c]
            syntax_error = True
            break
    
    # incomplete lines require closing characters which directly
    # correspond to the characters in each incomplete line
    if not syntax_error:
        line_score = 0
        for c in nl[::-1]: # score is computed in reverse
            line_score = (line_score * 5) + { '(': 1, '[': 2, '{': 3, '<': 4 }[c]
        scores_p2.append(line_score)
part1(score_p1)
part2(sorted(scores_p2)[len(scores_p2)//2])