#!/usr/bin/env python3

import sys
import collections
import re

input_lines = open('day8.txt','r').read().strip().split('\n')

sample = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""
sample = sample.strip().split('\n')

registers = collections.defaultdict(int)

def max_reg():
    return max(registers.items(),key=lambda x: x[1])

max_rval = 0
for inst in input_lines:
    m = re.match(r"^(\w+) (\w+) (-?\d+) if (\w+) (.*)$",inst)
    dr = m.group(1)
    cr = m.group(4)
    if eval(f"{registers[cr]}{m.group(5)}"):
        op = "+" if m.group(2) == 'inc' else "-"
        registers[dr] = eval(f"{registers[dr]} {op} {m.group(3)}")
    max_rval = max(max_rval,max_reg()[1])
#print(registers)
print(max_reg())

print(max_rval)

