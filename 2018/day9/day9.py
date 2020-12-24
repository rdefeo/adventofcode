#!/usr/bin/env python3

### Advent of Code - 2018 - Day 9

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


# Create a doubly-linked list since we have to go clockwise
# and counter-clockwise in our algorithm.
class Marble:
    def __init__(self,value):
        self.value = value
        self.next = self
        self.prev = self

# Fancy output like the problem statement - with the zero
# marble always at the front
def print_marbles(current):
    ptr = current
    while ptr.value != 0:
        ptr = ptr.next
    zero_marble = ptr   
    print(ptr.value,'',end='')
    ptr = ptr.next
    while ptr != zero_marble:
        print(f"({ptr.value}) ",end='') if ptr == current else print(f"{ptr.value} ",end='')
        ptr = ptr.next
    print('')
    
# Plays the game for (last_marble) turns
def marble_game(num_players,last_marble):
    current = Marble(0)
    #print_marbles(current)

    player = collections.defaultdict(int)
    for m in range(1,last_marble+1):
        if m % 23 != 0:
            left = current.next
            right = current.next.next
            marble = Marble(m)
            marble.next = right
            right.prev = marble
            left.next = marble
            marble.prev = left
            current = marble
        else:
            player[m%num_players] += m
            for _ in range(7):
                current = current.prev
            player[m%num_players] += current.value
            nc = current.next
            current.prev.next = nc
            nc.prev = current.prev
            current = nc
        #print_marbles(current)
    return max(player.items(),key=lambda x:x[1])

#part1(marble_game(9,25))

part1(marble_game(416,71975))

part2(marble_game(416,71975*100))