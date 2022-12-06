#!/usr/bin/env python3

### Advent of Code - 2022 - Day 6

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

examples = [
    'bvwbjplbgvbhsrlpgdmjqwftvncz',
    'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw' ]

PACKET = 4
MESSAGE = 14

def start_of(sig, distinct):
    for i in range(len(sig)):
        if len(set(sig[i:i+distinct])) == distinct:
            return i+distinct

# for e in examples:
#     print(start_of(e,PACKET))
#     print(start_of(e,MESSAGE))

part1(start_of(input_lines[0],PACKET))
part2(start_of(input_lines[0],MESSAGE))