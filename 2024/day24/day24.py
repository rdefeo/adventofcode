#!/usr/bin/env python3

### Advent of Code - 2024 - Day 24

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

inp1, inp2 = finput.split("\n\n")
wires = dict()
for line in inp1.split('\n'):
    w,v = line.split(':')
    wires[w] = int(v)

gates = dict()
max_zbit = 0
for line in inp2.split('\n'):
    l,op,r,_,o = line.split(' ')
    gates[o] = (op,l,r)
    if o[0] == 'z':
        max_zbit = max(max_zbit,int(o[1:]))
# print(max_zbit)

# For a given wire, check if it's the output of a gate.
# If not, return the original wire value
# Otherwise, recurse on the values of the left and right operands
# Apply the operator and return
def wire_value(w):
    if w not in gates:
        return wires[w]
    g,l,r = gates[w]
    l = wire_value(l)
    r = wire_value(r)
    if g == 'AND':
        return l & r
    elif g == 'OR':
        return l | r
    else:
        return l ^ r

# Part 1
# Straight forward recursive solver
zres = ''
for zb in range(max_zbit+1):
    w = 'z'+str(zb).zfill(2)
    v = wire_value(w)
    zres = str(v) + zres
part1(int(zres,2))


"""
Part 2 - Binary Adder
Inputs: A, B, Cin (Carry In)
Outputs: S (Sum), Cout (Carry Out)
             _____           _____
A ------+--\\ XOR \-----+--\\ XOR \--------- S
B ----+-|--//_____/  +--|--//_____/
      | |            |  |
Cin --|-|------------+  |   _____
      | |            |  +--[ AND )--+
      | |   _____    +-----[_____)  |   ____
      | +--[ AND )                  +--\ OR \-- Cout
      +----[_____)---------------------/____/


(A XOR B) XOR (Cin) = S
((A XOR B) AND Cin) OR (A AND B) = Cout

Since our first output bit, z00 has no Cin, there is no logic to compute Cout

From this diagram we can define some rules for the expected inputs and outputs
of the logic gates for every bit - making sure to account for the least significant and
most significant bit cases. Any wire that breaks these rules most likely needs to be
swapped.

1. Every Z output with X/Y inputs must be the result of an XOR
2. Every XOR that isn't directly acting on X/Y inputs must have a Z output
3. Ever Z output must be the result of an XOR (except z45)

The following rules ignore the 00 bit as that has no Carry Logic:
4. Every AND with X/Y inputs must have its output as the input to an OR
5. Every XOR with X/Y inputs must have its output as the input to an AND

"""
bad_wires = set()
for output in gates:
    op, l, r = gates[output]
    if output[0] == 'z' and op != 'XOR' and l[0] in 'xy' and r[0] in 'xy':
        bad_wires.add(output)
    elif op == 'XOR' and l[0] not in 'xy' and r[0] not in 'xy' and output[0] != 'z':
        bad_wires.add(output)
    elif output[0] == 'z' and op != 'XOR' and output != 'z'+str(max_zbit).zfill(2):
        bad_wires.add(output)
    elif op == 'AND' and l[0] in 'xy' and r[0] in 'xy' and l[1:] != '00':
        if not any([ins[0] == 'OR' and (output == ins[1] or output == ins[2]) for ins in gates.values()]):
            bad_wires.add(output)
    elif op == 'XOR' and l[0] in 'xy' and r[0] in 'xy' and l[1:] != '00':
        if not any([ins[0] == 'AND' and (output == ins[1] or output == ins[2]) for ins in gates.values()]):
            bad_wires.add(output)
part2(','.join(sorted(bad_wires)))
