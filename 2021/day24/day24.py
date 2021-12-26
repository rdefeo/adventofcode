#!/usr/bin/env python3

### Advent of Code - 2021 - Day 24

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

# Welp, this wasn't needed at all, but it's always fun to write a virtual machine!
class ALU():
    def __init__(self,monad,inp):
        self.pc = 0
        self.monad = monad
        self.input = str(inp)
        self.r = collections.defaultdict(int)
        self.debug = False
        self.error = ''
    def run(self):
        for line in self.monad:
            t = line.split()
            if t[0] == 'inp':
                i = self.input[0]
                self.input = self.input[1:]
                self.r[t[1]] = int(i)
                if self.debug: print(f"inp {t[1]} = {i}")
                if self.r['z'] != 0:
                    # print("invalid input - aborting")
                    self.error = 'invalid'
                    break
            elif t[0] == 'add':
                a = self.r[t[1]]
                b = self.r[t[2]] if t[2].isalpha() else int(t[2])
                self.r[t[1]] = a + b
                if self.debug: print(f"add {t[1]} = {a} + {b}")    
            elif t[0] == 'mul':
                a = self.r[t[1]]
                b = self.r[t[2]] if t[2].isalpha() else int(t[2])
                self.r[t[1]] = a * b
                if self.debug: print(f"mul {t[1]} = {a} * {b}")
            elif t[0] == 'div':
                a = self.r[t[1]]
                b = self.r[t[2]] if t[2].isalpha() else int(t[2])
                if b == 0:
                    print("DIV BY ZERO - abort")
                    self.r['z'] = 1
                    self.error = 'div by zero'
                    break
                self.r[t[1]] = a // b
                if self.debug: print(f"div {t[1]} = {a} // {b}")                    
            elif t[0] == 'mod':
                a = self.r[t[1]]
                b = self.r[t[2]] if t[2].isalpha() else int(t[2])
                if a < 0 or b <= 0:
                    print("MOD BY ZERO - abort")
                    self.r['z'] = 1
                    self.error = 'mod by zero'
                    break
                self.r[t[1]] = a % b
                if self.debug: print(f"mod {t[1]} = {a} % {b}")                    
            elif t[0] == 'eql':
                a = self.r[t[1]]
                b = self.r[t[2]] if t[2].isalpha() else int(t[2])
                self.r[t[1]] = int(a == b)
                if self.debug: print(f"eql {t[1]} = {a} == {b}")                    
            self.pc += 1
    def reset(self,inp):
        self.pc = 0
        self.r.clear()
        self.input = str(inp)
        self.error = ''

# The list of instructions essentially repeat every 18 lines with the only
# difference being the 3 values on lines 4, 5, and 15
constants = []
for i, line in enumerate(input_lines):
    if (i % 18) in [4, 5, 15]:
        constants.append(int(line.split()[2]))
for i in range(0,len(constants),3):
    print(constants[i:i+3])

# Those 3 values are used to compute the 'z' value, and this value is the
# only one of w,x,y,z to be carried forward with each computation. At the
# very end, the 'z' value must be zero to consider our input "valid"

# When looking at the algorithm in each block of instructions, the first
# value is a divisor. This divisor is only ever 1 or 26. Here are the values
# from my input:
#   [1, 12, 15]
#   [1, 14, 12]
#   [1, 11, 15]
#   [26, -9, 12]
#   [26, -7, 15]
#   [1, 11, 2]
#   [26, -1, 11]
#   [26, -16, 15]
#   [1, 11, 10]
#   [26, -15, 2]
#   [1, 10, 0]
#   [1, 12, 0]
#   [26, -4, 15]
#   [26, 0, 15]
#
# The algorithm for each section is as follows: (using zdiv, xadd, and yadd to represent
# the 3 values in each block)
# 
# def compute_z(w,z,zdiv,xadd,yadd):
#     if (z % 26) + xadd == w:
#         z //= zdiv
#     else:
#         z = ((z//zdiv)*26) + w + yadd
#     return z
#
# We can see that we are also multiplying and mod'ing z by 26. This is essentially treating
# z as a base 26 number. When the divisor is 1, the 2nd value is always > 10, and when it's 26,
# it's negative. This means when we reach the end, we want z to be one "digit" when performing
# the last divide by 26, in order to have it reach zero.

# Let's try building our model number one digit at a time using a DFS approach.
# Each block of instructions will either grow z by one digit or shrink it based
# on the divisor, zdiv. 

def solve_input(wrange, i, w, z, all_w):
    all_w = all_w + [w]
    zdiv,xadd,yadd = constants[i*3:i*3+3]
    # if we have a negative xadd, and thus a zdiv of 26 AND we will
    # fail the first check of our algo, then stop right here and return.
    # this prevents us from continuing to check wrong input values, greatly
    # reducing the runtime
    if xadd < 0 and (z % 26) + xadd != w:
        return False, []
    if (z % 26) + xadd == w: # first line of algo
        z //= zdiv
    else:
        z = ((z//zdiv)*26) + w + yadd

    if i == 13: # we're processing the last block of instructions - final check
        if z == 0:
            return True, all_w
        return False, []
    for new_w in wrange:
        r, w = solve_input(wrange, i+1, new_w, z, all_w)
        if r:
            return r, w
    return False, []

def solve(wrange):
    for w in wrange:
        r, w = solve_input(wrange, 0, w, 0, [])
        if r:
            return(''.join(map(str,w)))

# Part 1 - find maximum
part1(solve(range(9,0,-1)))

# Part 2 - find minimum
part2(solve(range(1,10)))