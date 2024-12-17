#!/usr/bin/env python3

### Advent of Code - 2024 - Day 17

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

i1, i2 = finput.split("\n\n")
R = [int(r[len("Register X: "):]) for r in i1.split("\n")]
P = list(map(int,i2[len("Program: "):].split(",")))

A, B, C = 0, 1, 2 # index into R

def combo(c):
    if c <= 3:
        return c
    if c != 7:
        return R[c-4]
    print("Invalid combo operand!")
    return None

# tests
# R, P = [0,0,9], [2, 6]
# R, P = [10, 0, 0], [5,0,5,1,5,4]
# R, P = [2024, 0, 0], [0,1,5,4,3,0]
# R, P = [0,29,0], [1,7]
# R, P = [0,2024,43690], [4,0]
def run_program(R,P):
    pc = 0
    output = []
    while 0 <= pc < len(P):
        op = P[pc]
        match op:
            case 0: # adv: A / 2**(combo(operand))
                R[A] = R[A] // 2**combo(P[pc+1])
            case 1: # bxl: B ^ operand
                R[B] = R[B] ^ P[pc+1]
            case 2: # bst: combo(operand) % 8
                R[B] = combo(P[pc+1]) % 8
            case 3: # jnz: jump to operand if A != 0
                if R[A] != 0:
                    pc = P[pc+1]
                    continue
            case 4: # bxc: B ^ C
                R[B] = R[B] ^ R[C]
            case 5: # out: 
                output.append(combo(P[pc+1])%8)
            case 6: # bdv
                R[B] = R[A] // 2**combo(P[pc+1])
            case 7: # cdv
                R[C] = R[A] // 2**combo(P[pc+1])
            case _:
                print("Invalid opcode!")
                break
        pc += 2
    return output

part1(','.join(list(map(str,run_program(R,P)))))


'''
Part 2
Our program, decoded a bit

Program: 2,4, 1,X1, 7,5, 1,X2, 0,3, 4,1, 5,5, 3,0 (hid some values)

BST A         B = A % 8
BXL 7         B = B ^ X1
CDV A // B    C = A // 2**B
BXL 7         B = B ^ X2
ADV 8         A = A // 8
BXC           B = B ^ C
OUT B         OUT B % 8
JNZ 0         JNZ to 0 if A != 0

From this we can see that A is essentially acting as our loop variable as it's constantly
divided by 8 and then tested in JNZ. Once it hits zero, we halt. Based on the numbers and
runtimes, we can't try *every* A value. Since smaller values of A are producing our last
output digits, we should be able to work backwards, by incrementing A. Also, every time we
try a new value of A, we don't need to reset B and C registers since those are both first
written to before they are read.

Let's keep multiplying our A by 8 and see if the resulting output matches the tail end of
our initial program. We also need to check the next 7 sequential values since a truncated
integer divide by 8 would procude the same A loop value, but with different values for B and
C. Only some of these test values will produce a matching program output - remember those
and then build upon them going forward. This should keep our search space smaller. Every
time we multiply an A value by 8, we ensure we'll output another digit.
'''

possible_A = [0]
for output_len in range(1,len(P)+1):
    next_possibles = []
    for a in [a * 8 + offset for a in possible_A for offset in range(2**3)]:
        R[A] = a 
        output = run_program(R,P)
        if output == P[-output_len:]:
            next_possibles.append(a)
    possible_A = next_possibles
part2(min(possible_A))