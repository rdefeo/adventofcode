#!/usr/bin/env python3

### Advent of Code - 2015 - Day 7

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

OP = {
    'AND': lambda x,y: (x&y)%65536,
    'OR': lambda x,y: (x+y)%65536,
    'LSHIFT': lambda x,y: (x<<y)%65536,
    'RSHIFT': lambda x,y: x>>y
}

def eval_circuit(part_2=False):
    wires = dict()
    signals = input_lines.copy()
    val = lambda x: wires[x] if x.isalpha() else int(x)
    while signals:
        # try to evaluate each signal - if we can, remove it from consideration
        s = signals.pop(0)
        t = s.split()
        if len(t) == 3: # assignment
            if t[0] in wires or t[0].isdigit():
                wires[t[2]] = val(t[0])
                if part_2 and t[2] == 'b': # Part 2 override
                    wires[t[2]] = 956
                continue
        if len(t) == 4: # NOT
            if t[1] in wires or t[1].isdigit():
                wires[t[3]] = (~val(t[1])) % 65536
                continue
        if (t[0] in wires or t[0].isdigit()) and (t[2] in wires or t[2].isdigit()):
            wires[t[4]] = OP[t[1]](val(t[0]),val(t[2]))
            continue
        signals.append(s) # not parsed, add it back to list
    return wires


part1(eval_circuit()['a'])
part2(eval_circuit(True)['a'])
        





