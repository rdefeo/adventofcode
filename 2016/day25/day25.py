#!/usr/bin/env python3

### Advent of Code - 2016 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
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

def gen_clock(inp):
    print("gen_clock",inp)
    R = {'a':inp,'b':0,'c':0,'d':0}
    
    def read(v):
        try:
            return int(v)
        except:
            return R[v]
    
    pc = 0
    out_count = 0
    last_out = None
    while 0 <= pc < len(input_lines):
        if out_count > 16:
            return True
        tokens = input_lines[pc].split(' ')
        # print(R,tokens)
        if tokens[0] == 'cpy':
            R[tokens[2]] = read(tokens[1])
        elif tokens[0] == 'inc':
            R[tokens[1]] += 1
        elif tokens[0] == 'dec':
            R[tokens[1]] -= 1
        elif tokens[0] == 'jnz':
            if read(tokens[1]) != 0:
                pc += read(tokens[2]) - 1
        elif tokens[0] == 'out':
            val = read(tokens[1])
            if last_out == None:
                last_out = val
                print(f"{inp}: first val is {val}")
            else:
                print(f"{inp}:  next val is {val}")
                if val == last_out:
                    return False
                last_out = val
                out_count += 1
        else:
            print("Unknown instruction!")
        pc += 1

for a in range(2000):
    if gen_clock(a):
        part1(a)
        break
