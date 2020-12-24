#!/usr/bin/env python3

import re
import functools
import collections
input = open('day13.txt','r').read().strip()

sample = """0: 3
1: 2
4: 4
6: 4"""

firewall = dict()
data = sample
data = input
for line in data.split('\n'):
    firewall[int(line.split(':')[0])] = int(line.split(': ')[1])

# one cycle of the scanner up and down a layer in the firewall
# is periodic based on it's depth. the period is 2*depth-2
# since, on every picosecond, we move from one layer to the next,
# the layer number we're currently on is the number of picoseconds
# elapsed.
# therefore, we just need to check if that layer/picosecond is
# evenly divisible by that layer's period
print("Part 1: ")
severity = 0
for pico,depth in firewall.items():
    if pico % (2*depth-2) == 0:
        severity += pico*depth
print(severity)

# same as Part 1, but this time, add a delay to our current
# layer/picosecond, until we're not caught
print("Part 2")
delay = 0
caught = False
while not caught:
    caught = True
    for pico,depth in firewall.items():
        if (pico+delay) % (2*depth-2) == 0:
            caught = False
            delay += 1
            break
print(delay)