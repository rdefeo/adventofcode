#!/usr/bin/env python3

### Advent of Code - 2016 - Day 4

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

sec_id_sum = 0
for room_id in input_lines:
    name, id, chksum = re.match(r'([a-z-]+)(\d+)\[(\w\w\w\w\w)\]',room_id).groups()
    name = name.replace('-','')
    c = collections.Counter(name)
    s = ''.join([k for k,_ in sorted(c.items(),key=lambda i: (-i[1],i[0]))[:5]])
    if s == chksum:
        sec_id_sum += int(id)
        # decrypt name
        shift = int(id) % 26
        d = ''.join([chr(ord('a') + ((ord(c)-ord('a')+shift)) % 26) for c in name])
        if 'pole' in d:
            part2(id)
part1(sec_id_sum)