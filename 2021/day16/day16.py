#!/usr/bin/env python3

### Advent of Code - 2021 - Day 16

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

inp = ''
for h in finput:
    inp += "{0:04b}".format(int(h,16))

OP = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda x: int(x[0]>x[1]),
    6: lambda x: int(x[0]<x[1]),
    7: lambda x: int(x[0]==x[1]),
}

versions = []
def parse(bits):
    global versions
    ver, id_type = (int(bits[0:3],2),int(bits[3:6],2))
    versions.append(ver)
    bits = bits[6:]
    if id_type == 4:
        # next group(s) of 5 bits are a literal value
        g = ''
        for i in range(0,len(bits),5):
            g += bits[i+1:i+5]
            if bits[i] == '0':
                bits = bits[i+5:]
                break
        return bits, int(g,2)
    else:
        # we have an operator
        op_len_type = bits[0]
        bits = bits[1:]
        if op_len_type == '0':
            # sub-packets are in next nb bits only
            nb = int(bits[0:15],2)
            bits = bits[15:]
            sub_bits = bits[:nb]
            res = []
            while sub_bits:
                sub_bits, value = parse(sub_bits)
                res.append(value)
            bits = bits[nb:]
        else:
            # parse next nb sub-packets
            nb = int(bits[0:11],2)
            bits = bits[11:]
            res = []
            for _ in range(nb):
                bits, value = parse(bits)
                res.append(value)
        return bits, OP[id_type](res)

p = parse(inp)
part1(sum(versions))
part2(p[1])


    


