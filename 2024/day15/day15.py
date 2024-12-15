#!/usr/bin/env python3

### Advent of Code - 2024 - Day 15

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


grid, moves = finput.split("\n\n")
grid = grid.split("\n")
moves = ''.join(moves.split("\n"))

# Instead of having a single solution that works on both parts, split it up
robot, robot2 = None, None
warehouse, warehouse_x2 = dict(), dict()
widen = { '#': '##', 'O': '[]', '.': '..' }
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == '@':
            robot = (x,y)
            robot2 = (x*2,y)
            c = '.'
        warehouse[(x,y)] = c
        warehouse_x2[(x*2,y)] = widen[c][0]
        warehouse_x2[(x*2+1,y)] = widen[c][1]
H, W = len(grid), len(grid[0])
W2 = W*2

dir = { '>': (1,0), 'v': (0,1), '<': (-1,0), '^': (0,-1) }

def print_warehouse(warehouse,width=W,robot=None):
    for y in range(H):
        for x in range(width):
            if robot == (x,y):
                print('@',end='')
            else:
                print(warehouse[(x,y)],end='')
        print()
    print()

# Part 1
# Straight forward robot movement and pushing
for m in moves:
    dx, dy = dir[m][0], dir[m][1]
    nx,ny = (robot[0]+dx, robot[1]+dy)
    if warehouse[(nx,ny)] == '.':
        robot = (nx,ny)
        continue
    if warehouse[(nx,ny)] == '#':
        continue
    # We've hit a box, see if we can push it forward. We might have a line of boxes
    # so find the end.
    while warehouse[(nx,ny)] == 'O':
        nx,ny = (nx+dx, ny+dy)
    # The next spot after our line of boxes is free, so move them
    if warehouse[(nx,ny)] == '.':
        # "move" all boxes between robot and nx, ny in our direction by simply
        # moving the next box to the end location
        robot = (robot[0]+dx, robot[1]+dy)
        warehouse[robot] = '.'
        warehouse[(nx,ny)] = 'O'

print_warehouse(warehouse)

def warehouse_sum(wh, box_type):
    wsum = 0
    for (x,y),b in wh.items():
        if b == box_type:
            wsum += x + 100*y
    return wsum
part1(warehouse_sum(warehouse,'O'))


# Part 2
# The warehouse is twice as wide. This doesn't greatly affect left/right pushes
# but makes up/down pushes more complex

# print_warehouse(warehouse_x2,W2,robot2)
for m in moves:
    # print(f"Move {m}")
    dx, dy = dir[m][0], dir[m][1]
    nx,ny = (robot2[0]+dx, robot2[1]+dy)
    if warehouse_x2[(nx,ny)] == '.':
        robot2 = (nx,ny)
        continue
    if warehouse_x2[(nx,ny)] == '#':
        continue
    # We've hit a box, see if we can push it forward
    if m in '<>' and warehouse_x2[(nx,ny)] in '[]':
        while warehouse_x2[(nx,ny)] in '[]':
            nx,ny = (nx+dx, ny+dy)
        if warehouse_x2[(nx,ny)] == '.':
            # Really move all boxes between robot and nx, ny in our direction
            # print(f"Found boxes between {x} and {robot2[0]+dx-1}")
            while nx != robot2[0]+dx:
                warehouse_x2[(nx,robot2[1])] = warehouse_x2[(nx-dx,robot2[1])]
                nx -= dx
            robot2 = (robot2[0]+dx, robot2[1]+dy)
            warehouse_x2[robot2] = '.'
    elif m in '^v' and warehouse_x2[(nx,ny)] in '[]':
        # For every row in our direction, keep track of a list of boxes we need to push
        boxes = []
        x = nx if warehouse_x2[(nx,ny)] == '[' else nx-1
        boxes.append([(x,ny)])
        can_move = True
        while can_move:
            blist = boxes[-1]
            # Algorithm is basically a BFS
            # check all the next spaces in the box's direction.
            #   if it's free we can move
            #   if it's blocked by a wall, we can't - stop checking
            #   if there's a box in front of is, add it to the list and keep checking
            next_boxes = []
            for b in blist:
                nx, ny = b[0]+dx, b[1]+dy
                if warehouse_x2[(nx,ny)] == '.' and warehouse_x2[(nx+1,ny)] == '.':
                    continue
                if warehouse_x2[(nx,ny)] == ']':
                    # box in front, to the left
                    next_boxes.append((nx-1,ny))
                if warehouse_x2[(nx,ny)] == '[':
                    # box directly in front
                    next_boxes.append((nx,ny))
                if warehouse_x2[(nx+1,ny)] == '[':
                    # box in front, to the right
                    next_boxes.append((nx+1,ny))
                if warehouse_x2[(nx,ny)] == '#' or warehouse_x2[(nx+1,ny)] == '#':
                    can_move = False
                    break
            # If we found boxes in front of us, add them and keep checking
            if next_boxes: 
                boxes.append(next_boxes)
            else:
                break

        if can_move:
            for blist in boxes[::-1]:
                for b in blist:
                    warehouse_x2[(b[0]+dx,b[1]+dy)] = '['
                    warehouse_x2[(b[0]+dx+1,b[1]+dy)] = ']'
                    warehouse_x2[b] = '.'
                    warehouse_x2[(b[0]+1,b[1])] = '.'
            robot2 = (robot2[0]+dx, robot2[1]+dy)
print_warehouse(warehouse_x2,W2,robot2)

part2(warehouse_sum(warehouse_x2,'['))
