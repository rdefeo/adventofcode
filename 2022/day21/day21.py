#!/usr/bin/env python3

### Advent of Code - 2022 - Day 21

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

expr = dict()
for line in input_lines:
    t, rest = line.split(': ')
    expr[t] = rest

def parse(ex):
    while True:
        tok = re.findall(r'[a-z]{4}',ex)
        if not tok:
            break
        for t in tok:
            ex = ex.replace(t,f"({expr[t]})")
    return ex

# Part 1
# Straight forward token replacement in the monkey expressions
part1(int(eval(parse('root'))))

# Part 2
# Some manual observations to help out here. First, we find which side of the 'root'
# equation our 'humn' is on. Then, evaluate the other side to get the total required
# for the equality. Then, keep checking possible values for 'humn' to see if we're
# getting close to that other side total.
#
# After testing some low numbers, I realized that our value needed to be MUCH larger.
# So I tried some absurdly large numbers until I found a possible range: lower to upper.
# Then it was just a matter of jumping around in that range to find the answer.

marker = -99999
expr['humn'] = marker
l = parse(expr['root'][:4])
r = parse(expr['root'][7:])

side = ''
val = 0
if str(marker) in l:
    side = l
    val = int(eval(r))
else:
    side = r
    val = int(eval(l))

guess = 0
jump = 100_000_000_000
while True:
    new_side = side.replace(str(marker),str(guess))
    new_val = int(eval(new_side))
    # print(guess, new_val)
    if new_val > val:   # not there yet
        guess += jump   # jump ahead
    elif new_val < val: # too far,
        guess -= jump   # go back
        jump //= 2      # shorten jump length
    else:
        part2(guess)
        break
