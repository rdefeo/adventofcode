#!/usr/bin/env python3

### Advent of Code - 2016 - Day 5

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


import hashlib

door_id = input_lines[0]

# Part 1
index = 0
password = ''
while True:
    h = hashlib.md5((door_id + str(index)).encode()).hexdigest()
    if h[:5] == '00000':
        print(index)
        password = password + h[5]
        if len(password) == 8:
            break;
    index += 1
part1(password)

# Part 2
index = 0
password = [' '] * 8
while True:
    h = hashlib.md5((door_id + str(index)).encode()).hexdigest()
    if h[:5] == '00000' and h[5].isdigit() and int(h[5]) <= 7:
        nh = int(h[5])
        if password[nh] == ' ':
            password[nh] = h[6]
            print(''.join(password))
            if ' ' not in password:
                break
    index += 1
part2(''.join(password))