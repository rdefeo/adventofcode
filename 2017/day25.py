#!/usr/bin/env python3

import collections
import sys
import re

infile = 'day25.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().strip()

tape = collections.defaultdict(int)
cursor = 0
instates = input.split('\n\n')

print(instates[0])
begin_state = instates[0].split('\n')[0][-2:-1]
print(begin_state)
steps = int(instates[0].split('\n')[1].split(' ')[-2:-1][0])
print(steps)

class State:
    def __init__(self,name,writes,moves,conts):
        self.name = name
        self.write = writes
        self.move = moves
        self.cont = conts

    def run(self):
        global tape
        global cursor
        cv = tape[cursor]
        tape[cursor] = self.write[cv]
        cursor += 1 if self.move[cv] == 'right' else -1
        return self.cont[cv]

states = dict()
for s in instates[1:]:
    m = re.match(r"In state (\w):",s)
    st = m.group(1)
    cvs = list(map(int,re.findall(r"current value is (\d+):",s)))
    writes = list(map(int,re.findall(r"Write the value (\d+).",s)))
    moves = re.findall(r"right|left",s)
    conts = re.findall(r"Continue with state (\w+).",s)
    state = State(st,writes,moves,conts)
    states[st] = state

curr_st = 'A'
for s in range(steps):
    st = states[curr_st]
    curr_st = st.run()
print(tape)
print(sum(x for x in tape.values()))