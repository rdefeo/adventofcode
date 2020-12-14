#!/usr/bin/env python3

### Advent of Code - 2020 - Day 14

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
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
#input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


# returns a (l) zero padded binary representation of number d
def dec2bin(d,l=36):
    return str(bin(int(d)))[2:].zfill(l)

mask = ''
mem = dict()

start_timer('part 1')
for x in input_lines:
    if x.startswith('mask = '):
        mask = x[len('mask = '):]
        continue
    m = re.match(r"mem\[(\d+)\] = (\d+)",x)
    if m:
        addr = int(m.group(1))
        val = dec2bin(m.group(2),36)
        result = ''.join([val[i] if b == 'X' else b for i,b in enumerate(mask)])
        mem[addr] = result

part1(sum([int(v,2) for k,v in mem.items()]))
stop_timer('part 1')

# reset mask and mem for part 2
mask = ''
mem = dict()

start_timer('part 2')
for x in input_lines:
    if x.startswith('mask = '):
        mask = x[len('mask = '):]
        continue
    m = re.match(r"mem\[(\d+)\] = (\d+)",x)
    if m:
        addr = dec2bin(m.group(1),36)
        bm = {'0':addr, '1':'1'*36, 'X':'F'*36}
        addr = ''.join([bm[b][i] for i,b in enumerate(mask)])
        floats = addr.count('F')

        val = dec2bin(m.group(2),36)

        # we have 'floats' floater bits. therefore we have 2^floats
        # possible addresses. generate 0..2^floats-1 and insert those
        # bits into addr at the floater bit locations
        for f in range(2**floats):
            fb = dec2bin(f,floats)
            newaddr = addr[:] # create copy
            fi = 0
            for i,b in enumerate(newaddr):
                if b == 'F':
                    newaddr = newaddr[:i] + fb[fi] + newaddr[i+1:]
                    fi += 1
            mem[int(newaddr,2)] = val

part2(sum([int(v,2) for k,v in mem.items()]))
stop_timer('part 2')