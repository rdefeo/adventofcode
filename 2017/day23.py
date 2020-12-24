#!/usr/bin/env python3

import collections
import sys

infile = 'day23.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().strip().split('\n')

NORMAL = 0
WAITING = 1
HALTED = 2
TERMINATED = 3
e2s = {NORMAL:"NORMAL",WAITING:"WAITING",HALTED:"HALTED",TERMINATED:"TERMINATED"}

def dd(d):
    return ','.join(f"{k}:{v}" for k,v in d.items())

class VM:
    def __init__(self,id,inst,part2=False):
        self.id = id
        self.inst = inst
        self.part2 = part2

        self.pc = 0
        self.registers = collections.defaultdict(int)
        self.mul_count = 0
        self.status = 0
        
    def dump(self):
        print('>>>',self.id,e2s[self.status],dd(self.registers),len(self.msgq_recv))

    def send(self,msg):
        self.msgq_recv.append(msg)

    def process_instruction(self):
        #self.dump()
        if 0 <= self.pc < len(self.inst):
            tokens = self.inst[self.pc].split(' ')
            #print(self.id,tokens)
            I = tokens[0]
            R = tokens[1]
            V = None if len(tokens) == 2 else tokens[2]
            if V:
                if str(V).isalpha():
                    V = self.registers[V]
                else:
                    V = int(V)
            if I == 'set':
                self.registers[R] = V
            elif I == 'sub':
                self.registers[R] -= V
            elif I == 'mul':
                self.mul_count += 1
                self.registers[R] *= V
            elif I == 'jnz': # jnz X Y
                if R.isalpha():
                    if self.registers[R] != 0:
                        self.pc += V
                        self.status = NORMAL
                        return
                else:
                    if int(R) != 0:
                        self.pc += V
                        self.status = NORMAL
                        return
            else:
                print("Unknown instruction!",self.inst[self.pc])
                quit()
            self.pc += 1
        else:
            print(self.id,"HALTING: PC out of range")
            self.status = HALTED
            quit()
            return None


    def run(self):
        c = 0
        while 0 <= self.pc < len(self.inst):
            c += 1
            self.process_instruction()
            if c % 1000 == 0:
                print(self.registers['h'])
            if self.status != NORMAL:
                break


# print("Part 1")
# vm = VM(0,input,False)
# print("RESULT:",vm.run())
# print(vm.mul_count)

import math
print("Part 2")
def isprime(n):
    for x in range(2,math.floor(math.sqrt(n)+1)):
        if n%x == 0:
            return False
    return True

h = 0
for b in range(108100,125100+1,17):
    if not isprime(b):
        h += 1
print(h)
