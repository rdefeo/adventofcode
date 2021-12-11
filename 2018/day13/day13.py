#!/usr/bin/env python3

### Advent of Code - 2018 - Day 13

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)



LEFT = (-1,0)
STRAIGHT = None
RIGHT = (1,0)
UP = (0,-1)
DOWN = (0,1)

CART_REPL = {'>':'-','<':'-','^':'|','v':'|'}
CART_STR = {RIGHT:'>',DOWN:'v',LEFT:'<',UP:'^'}

FACING = {'>':RIGHT,'v':DOWN,'<':LEFT,'^':UP}
TURN_R = {RIGHT:DOWN, DOWN:LEFT, LEFT:UP, UP:RIGHT}
TURN_L = {RIGHT:UP, UP:LEFT, LEFT:DOWN, DOWN:RIGHT}

TURN = {
    RIGHT: {'\\':DOWN,'/':UP,'-':RIGHT},
    UP: {'\\':LEFT,'/':RIGHT,'|':UP},
    LEFT: {'\\':UP,'/':DOWN,'-':LEFT},
    DOWN: {'\\':RIGHT,'/':LEFT,'|':DOWN}
    }

class Cart:
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.next_turn = LEFT
        self.facing = FACING[facing]
        self.auto = 0
        self.dead = False
    def __repr__(self):
        return f"{self.x},{self.y}: {CART_STR[self.facing]}"
    def move(self,loops):
        # move cart 'forward', make turns as necessary
        self.x,self.y = self.x+self.facing[0],self.y+self.facing[1]
        if loops[(self.x,self.y)] == '+':
            facing = [LEFT, STRAIGHT, RIGHT][self.auto]
            if facing == LEFT:
                self.facing = TURN_L[self.facing]
            elif facing == RIGHT:
                self.facing = TURN_R[self.facing]
            self.auto = (self.auto + 1) % 3
        else:
            self.facing = TURN[self.facing][loops[(self.x,self.y)]]

def print_loops(loops,carts):
    loops = loops.copy()
    min_x = min(l[0] for l in loops)
    min_y = min(l[1] for l in loops)
    max_x = max(l[0] for l in loops)
    max_y = max(l[1] for l in loops)
    for c in carts:
        loops[(c.x,c.y)] = CART_STR[c.facing] if loops[(c.x,c.y)] != 'X' else 'X'
        if c.dead:
            loops[(c.x,c.y)] = CART_STR[c.facing]
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(loops[(x,y)],end='')
        print('')
    print('')

# Parse the input loops and carts
loops = collections.defaultdict(lambda:' ')
carts = []
for y,l in enumerate(input_lines):
    for x in range(len(l)):
        loops[(x,y)] = l[x]
        if l[x] in '<>^v':
            carts.append(Cart(x,y,l[x]))
            loops[(x,y)] = CART_REPL[l[x]]


done = False
part1 = False
# print_loops(loops,carts)
while not done:
    # update the carts, making sure to process them in order
    carts = sorted(carts,key=lambda c:(c.y,c.x))
    # print([cart for cart in carts if not cart.dead])
    for c in carts:
        if c.dead: continue
        c.move(loops)
        # check if moving this one cart caused a crash
        for o in carts:
            if o == c or o.dead: continue
            if (o.x,o.y) == (c.x,c.y):
                print("CRASH! at",(o.x,o.y))
                if part1:
                    done = True
                # dead carts are removed from further moves
                o.dead = True
                c.dead = True
                break

    if not part1 and sum(not c.dead for c in carts) == 1:
        print([cart for cart in carts if not cart.dead])
        done = True
    # print_loops(loops,carts)
    