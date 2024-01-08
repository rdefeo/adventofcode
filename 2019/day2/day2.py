#!/usr/bin/env python3

### Advent of Code - 2019 - Day 2

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


master_program = list(map(int,finput.split(',')))
pc = 0
NORMAL, WAITING, HALTED, TERMINATED = "NORMAL", "WAITNG", "HALTED", "TERMINATED"

class IntCode:
    def __init__(self,prog,part2=False):
        self.program = prog.copy()
        self.part2 = part2
        self.pc = 0
        self.status = NORMAL
        self.inp = []
        self.output = []
        self.rb = 0 # relative base

    def get_value_at_ref(self,pos):
        return self.program[self.program[pos]]
    def get_value_at(self,pos):
        return self.program[pos]
    def get_value(self,pos,mode):
        # print(f"get {mode=} at {pos=} [{len(self.program)}]")
        if mode == 0:
            return self.program[self.program[pos]]
        elif mode == 1:
            return self.program[pos]
        elif mode == 2:
            return self.program[self.program[pos]+self.rb]
        print(f"GET: Invalid Mode {mode}")
        exit()
    def set_value(self,pos,mode,val):
        if mode == 0:   # position
            self.program[self.program[pos]] = val
        elif mode == 1: # immediate
            self.program[pos] = val
        elif mode == 2: # relative
            self.program[self.program[pos]+self.rb] = val
        else:
            print(f"SET: Invalid Mode: {mode}")

    def step(self):
        # print(self.program)
        if 0 <= self.pc < len(self.program):
            opcode = self.program[self.pc]
            op = opcode % 100
            modes = opcode // 100
            m1 = modes % 10
            modes = modes // 10
            m2 = modes % 10
            modes = modes // 10
            m3 = modes % 10

            # print(f"PC {self.pc}: {opcode} : {op} - {m1}, {m2}, {m3}")
            if op == 1: # addition
                a = self.get_value(self.pc+1,m1)
                b = self.get_value(self.pc+2,m2)
                # print(f"ADD {a}, {b} = {a+b}")
                self.set_value(self.pc+3,m3,a+b)
                self.pc += 4
            elif op == 2: # multiplication
                a = self.get_value(self.pc+1,m1)
                b = self.get_value(self.pc+2,m2)
                # print(f"MUL {a}, {b} = {a*b}")
                self.set_value(self.pc+3,m3,a*b)                
                self.pc += 4
            elif op == 99:
                #print(f"99 END: {self.program[0]}")
                self.status = TERMINATED
        else:
            self.status = HALTED
            print(f"{self.status}: PC out of range")
            exit()

    def run(self):
        while 0 <= self.pc < len(self.program):
            self.step()
            if self.status == TERMINATED or self.status == HALTED:
                #print("EXIT")
                break

program = master_program + [0 for _ in range(1000000)]

# Part 1
ic = IntCode(program,False)
ic.program[1] = 12
ic.program[2] = 2
ic.run()
part1(ic.program[0])

# Part 2
# Try all values for noun and verb until the result is equal to our target
for noun in range(100):
    for verb in range(100):
        #print(f"Trying {noun}, {verb}")
        ic = IntCode(program)
        ic.program[1] = noun
        ic.program[2] = verb
        ic.run()
        if ic.program[0] == 19690720:
            #print(noun,verb)
            part2(100*noun+verb)
            exit()
