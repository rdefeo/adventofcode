#!/usr/bin/env python3

### Advent of Code - 2024 - Day 7

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import operator

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

calc = {
    '+': operator.add,
    '*': operator.mul,
    '|': lambda x,y: int(str(x)+str(y))
}

def calibrate(avail_ops):
    total_result = 0
    for line in input_lines:
        result, operands = line.split(":")
        result = int(result)
        operands = list(map(int,operands.split()))

        for curr_op in itertools.product(avail_ops,repeat=len(operands)-1):
            res = operands[0]
            for op,val in zip(curr_op,operands[1:]):
                res = calc[op](res,val)
            if res == result:
                total_result += res
                break
    return total_result

part1(calibrate("+*"))
part2(calibrate("+*|"))

