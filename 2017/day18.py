#!/usr/bin/env python3

import collections
import sys

infile = 'day18.txt' if len(sys.argv)<2 else sys.argv[1]
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
        self.registers['p'] = id
        self.last_snd = None
        self.msgq_recv = []
        self.msgq_send = []
        self.send_count = 0
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
            elif I == 'add':
                self.registers[R] += V
            elif I == 'mul':
                self.registers[R] *= V
            elif I == 'mod':
                self.registers[R] %= V
            elif I == 'snd':
                self.send_count += 1
                if R.isalpha():
                    r = self.registers[R]
                else:
                    r = int(R)
                #print(self.id,"SENDING from",R,r)
                if self.part2:
                    self.msgq_send.append(r)
                else:
                    self.last_snd = r
            elif I == 'rcv':
                if self.part2:
                    if self.msgq_recv:
                        self.status = NORMAL
                        r = self.msgq_recv.pop(0)
                        self.registers[R] = r
                        #print(self.id,"RECEIVING into",R,r)
                    else:
                        #print(self.id,"RCV - no messages - WAITING")
                        self.status = WAITING
                        return
                else:
                    r = self.last_snd
                    if R.isalpha():
                        if self.registers[R] != 0:
                            #print(self.id,"RECEIVING (r)", r)
                            self.status = TERMINATED
                            return
                    else:
                        if int(R) != 0:
                            #print(self.id,"RECEIVING (v)", r)
                            self.status = TERMINATED
                            return
            elif I == 'jgz':
                if R.isalpha():
                    if self.registers[R] > 0:
                        self.pc += V
                        self.status = NORMAL
                        return
                else:
                    if int(R) > 0:
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
        while 0 <= self.pc < len(self.inst):
            self.process_instruction()
            if self.status != NORMAL:
                break
        if not self.part2 and self.status == TERMINATED:
            result = self.last_snd
            print(self.id,"Successful Termination",result)
            return result


print("Part 1")
vm = VM(0,input,False)
print("RESULT:",vm.run())

print("Part 2")

vm0 = VM(0,input,True)
vm1 = VM(1,input,True)

while True:
    if (vm0.status == WAITING and not vm0.msgq_recv) and (vm1.status == WAITING and not vm1.msgq_recv):
        print("DEADLOCK")
        break
    while vm0.status == NORMAL or vm0.msgq_recv:
        vm0.process_instruction()
    vm1.msgq_recv += vm0.msgq_send
    vm0.msgq_send = []
  
    while vm1.status == NORMAL or vm1.msgq_recv:
        vm1.process_instruction()
    vm0.msgq_recv += vm1.msgq_send
    vm1.msgq_send = []

print(vm1.id,"SENT:",vm1.send_count)
