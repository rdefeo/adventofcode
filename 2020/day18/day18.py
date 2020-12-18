#!/usr/bin/env python3

### Advent of Code - 2020 - Day 18

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

# operator precendence rules differ between Part 1 and Part 2
# Part 1: operators are equal
# Part 2: '+' beats '*'
def precedent(op1,op2,part):
    if part == 1:
        return True
    else:
        P = {'+':2,'*':1}
        return P[op1] >= P[op2]

def sum_exp(part):
    s = 0
    for x in input_lines:
        # Parse the Infix expression and convert to Postfix
        value = []
        op = []
        for c in x:
            if c.isspace():
                continue
            elif c.isdigit():
                #print(f"pushing num {c}")
                value.append(int(c))
            elif c == '+' or c == '*':
                #print(f"found op {c}")
                while len(op) != 0 and op[-1] not in '()' and precedent(op[-1],c,part):
                    o = op.pop()
                    a = value.pop()
                    b = value.pop()
                    #print(f" . eval {a} {o} {b}")
                    value.append(eval(f"{a} {o} {b}"))
                op.append(c)
            elif c == '(':
                #print("open paren")
                op.append(c)
            elif c == ')':
                #print("close paren")
                while len(op) != 0 and op[-1] != '(':
                    o = op.pop()
                    a = value.pop()
                    b = value.pop()
                    #print(f" . eval {a} {o} {b}")
                    value.append(eval(f"{a} {o} {b}"))
                op.pop()
            #print("s:", value)
            #print("o:", op)

        # Evaluate the Postfix expression represented by the two stacks: value and op
        while len(op) != 0:
            o = op.pop()
            a = value.pop()
            b = value.pop()
            value.append(eval(f"{a} {o} {b}"))
        assert len(op) == 0
        assert len(value) == 1
        #print(x," = ",value[0])
        s += value[0]
    return s
        
part1(sum_exp(1))

part2(sum_exp(2))