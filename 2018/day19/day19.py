#!/usr/bin/env python3

### Advent of Code - 2018 - Day 19

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

ip_set,instructions = input_lines[0],input_lines[1:]

registers = [0] * 6

count = 0
IP = 0
IPR = int(ip_set[-1])
# registers[0] = 1
while 0 <= IP < len(instructions):
    count += 1
    # if count > 5:
    #     break
    print(f"ip={IP} ",end='')
    print(' ',registers,end='')
    
    instr = instructions[IP]
    print(' ',instr,end='')

    registers[IPR] = IP
    op,a,b,c = instr.split(' ')[0],*list(map(int,instr.split(' ')[1:]))
    eval(op)(registers,a,b,c)
    IP = registers[IPR] + 1

    print(' ',registers,end='')
    print('')

part1(registers)