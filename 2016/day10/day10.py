#!/usr/bin/env python3

### Advent of Code - 2016 - Day 10

import sys
import requests
import re
import math
import itertools
import functools
import os

from aoc_utils import *
from collections import defaultdict

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

bot_values = defaultdict(list)
output_values = defaultdict(list)
bot_instr = defaultdict(list)

for x in input_lines:
    if x.startswith('value'):
        v,b = map(int,re.findall(r"\d+",x))
        bot_values[b].append(v)
    if x.startswith('bot'):
        b,b1,b2 = map(int,re.findall(r"\d+",x))
        to1,to2 = re.findall(r" (bot|output)",x)
        bot_instr[b] = (to1,b1),(to2,b2)

while bot_values:
    for k,v in dict(bot_values).items():
        if len(v) == 2:
            l,h = sorted(bot_values.pop(k))
            if l == 17 and h == 61: part1(k)
            (w1,v1),(w2,v2) = bot_instr[k]
            eval(w1+'_values')[v1].append(l)
            eval(w2+'_values')[v2].append(h)

part2(output_values[0][0]*output_values[1][0]*output_values[2][0])