#!/usr/bin/env python3

### Advent of Code - 2020 - Day 8

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections

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
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

instr = input_lines

start_timer('part 1')

# awwww, hell yeah. memories of 2019! implement a simple computer
# this time, the instructions only act on an accumulator
def run_prog(instr,code=-1):
    acc = 0
    pc = 0
    seen = set()
    while pc not in seen:
        seen.add(pc)
        if pc >= len(instr):
            return (True,acc)
        if instr[pc].startswith('nop'):
            #print('nop')
            pass
        if instr[pc].startswith('acc'):
            amt = int(input_lines[pc][3:])
            #print(f"acc {amt}")
            acc += amt
        if instr[pc].startswith('jmp'):
            amt = int(instr[pc][3:])
            #print(f"jmp {amt}")
            pc += amt
            continue
        pc += 1
    return (False,acc)

part1(run_prog(instr))

stop_timer('part 1')

start_timer('part 2')

# Run the same program as in part 1, many times. For each run, we will replace
# each 'nop' with 'jmp' and vice versa. So, create a generator function to do
# the needful. 
def gen_new_instr(instr):
    for line in range(len(instr)):
        if instr[line].startswith('nop'):
            new_instr = instr.copy()
            new_instr[line] = new_instr[line].replace('nop','jmp')
            yield new_instr
        elif instr[line].startswith('jmp'):
            new_instr = instr.copy()
            new_instr[line] = new_instr[line].replace('jmp','nop')
            yield new_instr

# for every possible iteration where we can replace 'nop'/'jmp', run the program
# if we detect that the program terminated successfully, we're done
for new_code in gen_new_instr(instr):
    result = run_prog(new_code)
    if result[0]:
        part2(result)

stop_timer('part 2')
