#!/usr/bin/env python3

### Advent of Code - 2015 - Day 6

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

funcs = {
    ('on',False): lambda _: True,
    ('off',False): lambda _: False, 
    ('toggle',False): lambda x: not x,
    ('on',True): lambda x: x+1,
    ('off',True): lambda x: max(0,x-1), 
    ('toggle',True): lambda x: x+2
}

def apply_func(l,n,func):
    for x in range(n[0],n[2]+1):
        for y in range(n[1],n[3]+1):
            l[(x,y)] = func(l[(x,y)])
    return l

def solve(part2=False):
    lights = collections.defaultdict(int)
    for inst in input_lines:
        nums = list(map(int,re.findall(r"\d+",inst)))
        if inst.startswith('turn on'):
            lights = apply_func(lights,nums,funcs[('on',part2)])
        elif inst.startswith('turn off'):
            lights = apply_func(lights,nums,funcs[('off',part2)])
        else:
            lights = apply_func(lights,nums,funcs[('toggle',part2)])
    return sum(lights.values())

part1(solve())
part2(solve(True))