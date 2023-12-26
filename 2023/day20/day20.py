#!/usr/bin/env python3

### Advent of Code - 2023 - Day 20

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

LO, HI = 0, 1
OFF, ON = 0, 1

modules = dict() # name -> Module
pending_pulses = []
lo_count, hi_count = 0, 0
button_pushes = 0

class Module:
    def __init__(self, name, recv=[]):
        self.name = name
        self.im = []
        self.om = recv
        self.pending_pulse = None
    def __repr__(self):
        return str(self.im) + " -> " + self.name + " -> " + str(self.om)
    def receive(self, name, pulse):
        # Used for debugging
        # print(f"{name} -{['low','high'][pulse]}-> {self.name}")
        pass
    def send_pulse(self):
        global lo_count, hi_count
        for o in self.om:
            modules[o].receive(self.name, self.pending_pulse)
            if self.pending_pulse == LO:
                lo_count += 1
            else:
                hi_count += 1

class Button(Module):
    def __init__(self, name, recv=["broadcaster"]):
        Module.__init__(self,name,recv)
    def push(self, pulse=LO):
        global button_pushes
        button_pushes += 1
        self.pending_pulse = pulse
        self.send_pulse()

class Broadcaster(Module):
    def __init__(self, name, recv=[]):
        Module.__init__(self,name,recv)
    def receive(self, name, pulse):
        Module.receive(self, name, pulse)
        self.pending_pulse = pulse
        pending_pulses.append(self.name)

class FlipFlop(Module):
    def __init__(self, name, recv):
        Module.__init__(self, name, recv)
        self.state = OFF
    def receive(self, name, pulse):
        Module.receive(self, name, pulse)
        if pulse == LO:
            if self.state == OFF:
                self.state = ON
                self.pending_pulse = HI
            else:
                self.state = OFF
                self.pending_pulse = LO
            pending_pulses.append(self.name)

class Conjuction(Module):
    def __init__(self, name, recv):
        Module.__init__(self, name, recv)
        # All Conjuction modules have a default LO pulse for every input module
        self.im_last_pulse = collections.defaultdict(lambda:LO)
        self.im_pulse_flipped = collections.defaultdict(int)
    def receive(self, name, pulse):
        Module.receive(self, name, pulse)
        
        # For Part 2, we care about when a conjuction has one of its inputs
        # flip from LO to HI. As when all inputs are HI, we output a LO.
        # Therefore, record *when* this input flips
        if pulse == HI and self.im_pulse_flipped[name] == 0:
            self.im_pulse_flipped[name] = button_pushes

        self.im_last_pulse[name] = pulse
        if sum(self.im_last_pulse.values()) == len(self.im):
            self.pending_pulse = LO
        else:
            self.pending_pulse = HI
        pending_pulses.append(self.name)

def read_module_data():
    """ Parse input file and create modules by type. Since we only know
    the module name and its receivers, we then have to keep track of all
    non-senders and create default Modules for them. Lastly we need to
    iterate over all modules and assign our inputs. """
    global pending_pulses, lo_count, hi_count, button_pushes
    mods = dict()
    pending_pulses = []
    lo_count, hi_count = 0, 0
    button_pushes = 0

    all_outputs = set()
    for line in input_lines:
        name, receivers = line.split(' -> ')
        receivers = receivers.split(', ')
        if name.startswith('&'):
            mods[name[1:]] = Conjuction(name[1:],receivers)
        elif name.startswith('%'):
            mods[name[1:]] = FlipFlop(name[1:],receivers)
        elif name == "broadcaster":
            mods[name] = Broadcaster(name,receivers)
        all_outputs.update(receivers)
    for o in all_outputs:
        if o not in mods:
            mods[o] = Module(o)
    mods["button"] = Button("button")
    mods["broadcaster"].im = ["button"]

    # Setup inputs to each module
    for m in mods.values():
        for o in m.om:
            if o in mods and m.name not in mods[o].im:
                mods[o].im.append(m.name)
            # Create untyped modules for output-only nodes
            if o not in mods:
                mods[o] = Module(o)    
    return mods

# Part 1
modules = read_module_data()
for _ in range(1000):
    modules["button"].push()
    while pending_pulses:
        m = pending_pulses.pop(0)
        modules[m].send_pulse()
part1(lo_count * hi_count)

# Part 2
# From reading our input, we see that 'rx' is fed by a conjuction. And the
# only way for that to send us a LO is if all of its inputs are HI. Therefore
# we need to know which Button push makes each of those inputs flip to HI.

# Find who sends a pulse to 'rx', as this is the module we want to monitor
# for when it would possibly emit a LO.
modules = read_module_data()
rx_input = modules[modules['rx'].im[0]]
while True:
    modules["button"].push()
    while pending_pulses:
        m = pending_pulses.pop(0)
        modules[m].send_pulse()
    if len(rx_input.im) == len(rx_input.im_pulse_flipped) and all(rx_input.im_pulse_flipped.values()):
        part2(math.lcm(*rx_input.im_pulse_flipped.values()))
        break
