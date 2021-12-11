#!/usr/bin/env python3

### Advent of Code - 2018 - Day 21

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
    # return R
def addi(R,a,b,c):
    R[c] = R[a]+b
    # return R
def mulr(R,a,b,c):
    R[c] = R[a]*R[b]
    # return R
def muli(R,a,b,c):
    R[c] = R[a]*b
    # return R
def banr(R,a,b,c):
    R[c] = R[a]&R[b]
    # return R
def bani(R,a,b,c):
    R[c] = R[a]&b
    # return R
def borr(R,a,b,c):
    R[c] = R[a]|R[b]
    # return R
def bori(R,a,b,c):
    R[c] = R[a]|b
    # return R
def setr(R,a,b,c):
    R[c] = R[a]
    # return R
def seti(R,a,b,c):
    R[c] = a
    # return R
def gtir(R,a,b,c):
    R[c] = 1 if a > R[b] else 0
    # return R
def gtri(R,a,b,c):
    R[c] = 1 if R[a] > b else 0
    # return R
def gtrr(R,a,b,c):
    R[c] = 1 if R[a] > R[b] else 0
    # return R
def eqir(R,a,b,c):
    R[c] = 1 if a == R[b] else 0
    # return R
def eqri(R,a,b,c):
    R[c] = 1 if R[a] == b else 0
    # return R
def eqrr(R,a,b,c):
    R[c] = 1 if R[a] == R[b] else 0
    # return R    

opcodes = [
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
    ]

ip_set,instructions = input_lines[0],input_lines[1:]

commands = []
for i in instructions:
    op,a,b,c = i.split(' ')[0],*list(map(int,i.split(' ')[1:]))
    commands.append((op,[a,b,c]))

registers = [0] * 6
IP = 0
IPR = int(ip_set[-1])

p1 = 11592302
p2 = 313035
# registers[0] = p1
count = 0
seen = set()
last = None
part_1 = False
while 0 <= IP < len(commands):
    if IP == 28:
        if part_1:
            print(registers)
            part1(registers[1]) # R1
            quit()
        else:
            if registers[1] in seen:
                print("LOOPED!")
                break
            
            last = registers[1]
            part2(last)
            seen.add(last)
        # break
    # print(f"ip={IP} ",end='')
    
    cmd = commands[IP]
    # print(' ',instr,end='')

    registers[IPR] = IP
    # op,a,b,c = instr.split(' ')[0],*list(map(int,instr.split(' ')[1:]))
    eval(cmd[0])(registers,*cmd[1])
    # eval(op)(registers,a,b,c)
    count += 1
    IP = registers[IPR] + 1

    # print(' ',registers,end='')
    # print('')

