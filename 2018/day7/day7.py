#!/usr/bin/env python3

### Advent of Code - 2018 - Day 7

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
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

instr = []
for a in input_lines:
    m = re.findall(r"tep (\w) ",a)
    instr.append((m[0],m[1]))

# full list of all nodes in our graph
steps = {s for step_pair in instr for s in step_pair}
#print(steps)

def find_next_steps(steps,instr):
    next_steps = [step for step in steps if all(s != step for _,s in instr)]
    return sorted(next_steps)

# Part 1
path = []
while steps:
    next_step = find_next_steps(steps,instr)[0]
    path.append(next_step)
    steps.remove(next_step)
    instr = [(pre,s) for (pre,s) in instr if pre != next_step]
part1(''.join(path))


# Part 2
# re-initialize instr and steps
for a in input_lines:
    m = re.findall(r"tep (\w) ",a)
    instr.append((m[0],m[1]))
steps = {s for step_pair in instr for s in step_pair}

def step_duration(s):
    return (ord(s) - ord('A') + 1) + 60

time = -1
workers = [{'step':None,'time':0} for _ in range(5)]
while steps or any(w['time'] > 0 for w in workers):
    for w in workers:
        w['time'] = max(w['time']-1,0)
        if w['time'] == 0: # we completed a task
            if w['step'] is not None:
                # remove any steps which have our current task step
                # as a pre-requisite
                instr = [(pre,s) for (pre,s) in instr if pre != w['step']]
                w['step'] = None
            next_steps = find_next_steps(steps,instr)
            if next_steps:
                step = next_steps.pop(0)
                w['time'] = step_duration(step)
                w['step'] = step
                steps.remove(step)
    time += 1
part2(time)