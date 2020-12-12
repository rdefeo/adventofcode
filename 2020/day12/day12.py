#!/usr/bin/env python3

### Advent of Code - 2020 - Day 12

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
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
#input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

EAST = (1,0)
SOUTH = (0,-1)
WEST = (-1,0)
NORTH = (0,1)

turn = {
    'L':{ EAST:NORTH, NORTH:WEST, WEST:SOUTH, SOUTH:EAST },
    'R':{ EAST:SOUTH, SOUTH:WEST, WEST:NORTH, NORTH:EAST }
    }
rotate = { 'L':(-1,1), 'R':(1,-1) }

class Ship():
    def __init__(self,part=1):
        self.facing = EAST
        self.x = 0
        self.y = 0
        self.wp = [10,1]
        self.part = part
    def forward(self,amt):
        if self.part == 1:
            self.x += (self.facing[0]*amt)
            self.y += (self.facing[1]*amt)
        else:
            self.x += (self.wp[0]*amt)
            self.y += (self.wp[1]*amt)
    def shift(self,d,amt):
        if d == 'E':
            if self.part == 1:
                self.x += amt
            else:
                self.wp[0] += amt
        elif d == 'S':
            if self.part == 1:
                self.y -= amt
            else:
                self.wp[1] -= amt
        elif d == 'W':
            if self.part == 1:
                self.x -= amt
            else:
                self.wp[0] -= amt
        elif d == 'N':
            if self.part == 1:
                self.y += amt
            else:
                self.wp[1] += amt
    def turn(self,d,amt):
        a = amt // 90
        if amt % 90 != 0:
            print(f"Ugly angle: {amt}")
            quit()
        #print(f"turning {d}, {a}")
        for _ in range(a):
            if self.part == 1:
                self.facing = turn[d][self.facing]
            else:
                # swap x,y and multiply by rotation
                self.wp = [n*self.wp[::-1][i] for i,n in enumerate(rotate[d])]
    def move(self,d,a):
        if d == 'F':
            self.forward(int(a))
        elif d in "NESW":
            self.shift(d,a)
        elif d == 'L' or d == 'R':
            self.turn(d,a)
    def manhattan(self):
        return abs(self.x)+abs(self.y)

def travel(ship):
    for x in input_lines:
        ship.move(x[0],int(x[1:]))
        #print(f"{ship.x}, {ship.y}, {ship.facing}")
    eval(f"part{ship.part}")(ship.manhattan())

ship = Ship(1)
travel(ship)

ship = Ship(2)
travel(ship)


