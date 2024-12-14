#!/usr/bin/env python3

### Advent of Code - 2024 - Day 14

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

W, H = 101, 103
robots = []
vels = []
for line in input_lines:
    m = list(map(int,re.findall(r"(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)",line)[0]))
    p,v = m[:2],m[2:]
    robots.append(tuple(p))
    vels.append(tuple(v))

def print_robots(robots):
    final = collections.Counter(robots)
    for y in range(H):
        for x in range(W):
            if (x,y) in final:
                print(f"{final[(x,y)]}",end='')
            else:
                print(".",end='')
        print()
    print()
   
min_score = math.inf
min_score_time = 0
for t in range(1,10000):
    for r,(p,v) in enumerate(zip(robots,vels)):
        robots[r] = ((p[0]+v[0])%W, (p[1]+v[1])%H)

    final = collections.Counter(robots)
    q1 = sum(c for p,c in final.items() if p[0] < W//2 and p[1] < H//2)
    q2 = sum(c for p,c in final.items() if p[0] > W//2 and p[1] < H//2)
    q3 = sum(c for p,c in final.items() if p[0] < W//2 and p[1] > H//2)
    q4 = sum(c for p,c in final.items() if p[0] > W//2 and p[1] > H//2)
    safety = q1*q2*q3*q4
    
    # Part 1
    if t == 100:
        part1(safety)

    # Part 2
    #  Approach 1:
    # Assume that to make a Christmas tree, no robots will be overlapping
    # c = collections.Counter(robots)
    # if len(c) == len(robots):
    #     print_robots(robots)
    #     part2(t)
    #     break

    #  Approach 2:
    # When the robots are clustered to form the tree, there will be fewer in some
    # quadrants, thus lowering the safety score. Find the time when we have the
    # lowest safety score!
    if safety < min_score:
        min_score = safety
        min_score_time = t
        print(safety,q1,q2,q3,q4)

    if t == 8258:
        print_robots(robots)
part2(min_score_time)
