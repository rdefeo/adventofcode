#!/usr/bin/env python3

### Advent of Code - 2015 - Day 11

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

def pw_inc(pw):
    pw = list(pw)
    for l in range(len(pw)-1,-1,-1):
        if pw[l] == 'z':
            pw[l] = 'a'
            continue
        else:
            pw[l] = chr(ord(pw[l])+1)
            break
    return ''.join(pw)

def first_req(pw):
    ab = 'abcdefghijklmnopqrstuvwxyz'
    for trip in [ab[i:i+3] for i in range(0,len(ab)-2)]:
        if trip in pw:
            return True
    return False

def second_req(pw):
    return not any(l in 'iol' for l in pw)

def third_req(pw):
    d = re.findall(r"(\w)(\1)",pw)
    if len(d) >= 2 and d[0] != d[1]:
        return True
    return False

def pw_passes(pw):
    return first_req(pw) and second_req(pw) and third_req(pw)

pw = finput
while not pw_passes(pw):
    pw = pw_inc(pw)
part1(pw)    

pw = pw_inc(pw)
while not pw_passes(pw):
    pw = pw_inc(pw)
part2(pw)
