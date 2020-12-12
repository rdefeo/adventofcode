# aoc_utils

import time
from enum import Enum

# terminal colors
DRED = '\033[91m'
RED = '\033[91m'
DGREEN = '\033[32m'
GREEN = '\033[92m'
DBLUE = '\033[34m'
YELLOW = '\033[33m'
BLUE = '\033[94m'
LBLUE = '\033[36m'
DCYAN = '\033[36m'
CYAN = '\033[96m'
DPURPLE = '\033[35m'
PURPLE = '\033[95m'
CLEAR = '\033[39m'

# simple timer functions
timers = {}
def start_timer(n=0):
    timers[n] = time.time()
def stop_timer(n=0):
    if n in timers:
        msg = f".timer ({n}): " if n != 0 else "total time: "
        print(DCYAN+msg+CYAN+"{:.3f}".format(time.time()-timers[n])+CLEAR)
        timers.pop(n)
    else:
        print(RED+f"error: timer {n} was not started"+CLEAR)

# output
def part1(s='no output!'):
    print(DPURPLE+"Part 1: "+PURPLE+str(s)+CLEAR)
def part2(s='no output!'):
    print(DPURPLE+"Part 2: "+PURPLE+str(s)+CLEAR)


class Dir(Enum):
    UP = [-1,0]
    RIGHT = [0,1]
    DOWN = [1,0]
    LEFT = [0,-1]
    NORTH = [-1,0]
    EAST = [0,1]
    SOUTH = [1,0]
    WEST = [0,-1]

class Grid:
    def __init__(self,lines=[]):
        self.lines = [line.rstrip() for line in lines]
        self.width = len(lines[0])
        self.height = len(lines)
        self.pos = [0,0] # ROW, COL

    def set_pos(self,p=[0,0]):
        if self.in_grid(p):
            print("setting pos")
            self.pos = p

    def set_row_pos(self,row):
        np = [row,self.pos[1]]
        if self.in_grid(np):
            self.pos[0] = row

    def set_col_pos(self,col):
        np = [self.pos[0],col]
        if self.in_grid(np):
            self.pos[0] = col

    def in_grid(self,p):
        if p[0] < 0 or p[0] >= self.height:
            return False
        if p[1] < 0 or p[1] >= self.width:
            return False
        return True

    def move(self,dir,dist=1):
        if dist == 0:
            return
        d = dir.value
        newpos = [self.pos[0]+(d[0]*dist), self.pos[1]+(d[1]*dist)]
        if self.in_grid(newpos):
            self.pos = newpos
            
    def print(self,pos_highlight=True):
        if pos_highlight:
            for r in range(self.height):
                for c in range(self.width):
                    if self.pos == [r,c]:
                        print(DGREEN+f"{self.lines[r][c]}"+CLEAR,end='')
                    else:
                        print(f"{self.lines[r][c]}",end='')
                print('')
        else:
            print('\n'.join(self.lines))

    def print_pos(self):
        print(f"grid pos: r={self.pos[0]}, c={self.pos[1]}")