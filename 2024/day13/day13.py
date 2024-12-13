#!/usr/bin/env python3

### Advent of Code - 2024 - Day 13

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

# Return the intersection if line AB with line CD
def line_intersection(A,B,C,D):
    a = (D[0]-C[0]) * (C[1]-A[1]) - (D[1]-C[1]) * (C[0]-A[0])
    b = (D[0]-C[0]) * (B[1]-A[1]) - (D[1]-C[1]) * (B[0]-A[0])
    alpha = a/b
    return (A[0]+alpha*(B[0]-A[0]), A[1]+alpha*(B[1]-A[1]))

tokens = [0, 0]
for m in finput.split("\n\n"):
    a,b,p = m.split("\n")
    a = tuple(map(int,re.findall(r"\+(\d+).*\+(\d+)",a)[0]))
    b = tuple(map(int,re.findall(r"\+(\d+).*\+(\d+)",b)[0]))
    p = tuple(map(int,re.findall(r"=(\d+).*=(\d+)",p)[0]))
    # print(a,b,p)

    # Prize locations for Part 1 and Part 2
    p1 = p
    p2 = (p[0]+10000000000000,p[1]+10000000000000)
    
    for i, p in enumerate([p1, p2]):
        # line with slope B coming from prize
        pb = (p[0]-b[0],p[1]-b[1])

        I = line_intersection((0,0),a,p,pb)
        # How many times does it take a to reach intersection
        a2i = I[0] / a[0]
        # How many times does it take b to reach intersection (from p)
        b2i = (p[0]-I[0]) / b[0] 
        # If both number of steps are whole numbers, add-em up
        if float(a2i).is_integer() and float(b2i).is_integer():
            tokens[i] += a2i * 3 + b2i * 1
    
part1(int(tokens[0]))
part2(int(tokens[1]))


