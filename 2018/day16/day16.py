#!/usr/bin/env python3

### Advent of Code - 2018 - Day 16

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

# define our opcodes
def addr(R,a,b,c):
    R[c] = R[a]+R[b]
    return R
def addi(R,a,b,c):
    R[c] = R[a]+b
    return R
def mulr(R,a,b,c):
    R[c] = R[a]*R[b]
    return R
def muli(R,a,b,c):
    R[c] = R[a]*b
    return R
def banr(R,a,b,c):
    R[c] = R[a]&R[b]
    return R
def bani(R,a,b,c):
    R[c] = R[a]&b
    return R
def borr(R,a,b,c):
    R[c] = R[a]|R[b]
    return R
def bori(R,a,b,c):
    R[c] = R[a]|b
    return R
def setr(R,a,b,c):
    R[c] = R[a]
    return R
def seti(R,a,b,c):
    R[c] = a
    return R
def gtir(R,a,b,c):
    R[c] = 1 if a > R[b] else 0
    return R
def gtri(R,a,b,c):
    R[c] = 1 if R[a] > b else 0
    return R
def gtrr(R,a,b,c):
    R[c] = 1 if R[a] > R[b] else 0
    return R
def eqir(R,a,b,c):
    R[c] = 1 if a == R[b] else 0
    return R
def eqri(R,a,b,c):
    R[c] = 1 if R[a] == b else 0
    return R
def eqrr(R,a,b,c):
    R[c] = 1 if R[a] == R[b] else 0
    return R    

opcodes = [
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
    ]

instructions,program = input.split('\n\n\n\n')

sample_count = 0
codemap = collections.defaultdict(set)
for sample in instructions.split('\n\n'):
    before,instr,after = sample.split('\n')
    
    # for each sample, run it through all 16 instructions to see what matches
    # then count how many match 3 or more instructions
    bef = list(map(int,re.findall(r"\d+",before)))
    instr = list(map(int,instr.split(' ')))
    aft = list(map(int,re.findall(r"\d+",after)))
    opcount = 0
    for op in opcodes:
        if op(bef.copy(),*instr[1:]) == aft:
            opcount += 1
            codemap[instr[0]].add(op)
    if opcount >= 3:
        sample_count += 1
    # quit()
part1(sample_count)

instmap = dict()
while codemap:
    for o,c in codemap.items():
        if len(c) == 1:
            instmap[o] = min(c)
    for i in instmap:
        if i in codemap:
            codemap.pop(i)
            for c in codemap:
                codemap[c].discard(instmap[i])

registers = [0]*4
for line in program.split('\n'):
    instr = list(map(int,line.split(' ')))
    registers = instmap[instr[0]](registers,*instr[1:])
part2(registers)
