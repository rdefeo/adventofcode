#!/usr/bin/env python3

### Advent of Code - 2022 - Day 11

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from copy import deepcopy

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

class Monkey():
    def __init__(self):
        self.items = []
        self.op = '' # new = old */+ int or old
        self.test_div = 0 # always "is divisible by X"
        self.throw_true = 0
        self.throw_false = 0
        self.inspect_count = 0
    def test(self,item):
        return (item % self.test_div == 0)
    def operation(self,item):
        if "old" in self.op:
            return item * item
        else:
            return eval(str(item)+self.op)

monkeys = []
super_modulo = 1
for line in input_lines:
    m = -1
    if "Monkey" in line:
        m += 1
        monkeys.append(Monkey())
    if "items" in line:
        monkeys[m].items = list(map(int,re.findall(r'\d+',line)))
    if "Operation" in line:
        monkeys[m].op = line[21:]
    if "Test" in line:
        d = int(re.findall(r'(\d+)',line)[0])
        monkeys[m].test_div = d
        super_modulo *= d
    if "true" in line:
        t = int(re.findall(r'(\d+)',line)[0])
        monkeys[m].throw_true = t
    if "false" in line:
        t = int(re.findall(r'(\d+)',line)[0])
        monkeys[m].throw_false = t
p2_monkeys = deepcopy(monkeys)

def monkey_round(monkeys, part2):
    for i,m in enumerate(monkeys):
        while m.items:
            item = m.items.pop(0)
            item = m.operation(item)
            if part2:
                item %= super_modulo
            else:
                item //= 3
            if m.test(item):
                monkeys[m.throw_true].items.append(item)
            else:
                monkeys[m.throw_false].items.append(item)
            m.inspect_count += 1
    return monkeys

def run_part(monks,rounds,p2,printfn):
    for r in range(rounds):
        monks = monkey_round(monks,p2)
    for i,m in enumerate(monkeys):
        print(f"Monkey {i}: {m.items}")
    insp = sorted([m.inspect_count for m in monks],reverse=True)
    print(insp)
    printfn(insp[0]*insp[1])
    
run_part(monkeys,20,False,part1)

run_part(p2_monkeys,10000,True,part2)
