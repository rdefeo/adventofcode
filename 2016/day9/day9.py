#!/usr/bin/env python3

### Advent of Code - 2016 - Day 9

import sys
import requests
import re
import math
import itertools
import functools
import os

from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

p1 = 0
p2 = 0

uncomp = ''
comp = input
need_to_decomp = True

i = 0
while i < len(comp):
    #print(uncomp)
    if comp[i] != '(':
        uncomp += comp[i]
        i += 1
        continue
    m = re.match(r"\((\d+)x(\d+)\)", comp[i:])
    if m:
        skip = len(m.group(0))
        c = int(m.group(1))
        r = int(m.group(2))
        #print(f"skip {skip}, c {c}, r {r}")
        data = comp[i+skip:i+skip+c]
        #print(f"data {data}")
        for _ in range(r):
            uncomp += data
        i += skip+c
   
#print(uncomp)
part1(len(uncomp))

comp = input
uncomp = (0, comp)  # uncompressed bytes, followed by compressed data

def uncompress(s):
    m = re.search(r"\((\d+)x(\d+)\)",s)
    if not m:
        return len(s) # end of string, no more repeated patterns
    length = int(m.group(1))
    times = int(m.group(2))
    start = m.start() + len(m.group())
    count = uncompress(s[start:start+length])

    #       prefix of AxB          B * recurse    uncompress postfix of AxB
    return (len(s[:m.start()]) + times*count + uncompress(s[start+length:]))

part2(uncompress(comp))
quit()

i = 0
while i < len(comp):
    #print(uncomp)
    if comp[i] != '(':
        uncomp[0] += 1
        i += 1
        continue
    m = re.match(r"\((\d+)x(\d+)\)", comp[i:])
    if m:
        skip = len(m.group(0))
        c = int(m.group(1))
        r = int(m.group(2))
        print(f"skip {skip}, c {c}, r {r}")
        data = comp[i+skip:i+skip+c]
        print(f"data {data}")
        for _ in range(r):
            uncomp += data
        i += skip+c

part2(uncomp[0])

