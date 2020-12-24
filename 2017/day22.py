#!/usr/bin/env python3

import re
import sys
import collections

infile = 'day22.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().split('\n')

grid = collections.defaultdict(lambda:'.')

UP = (0,-1)
RIGHT = (1,0)
DOWN = (0,1)
LEFT = (-1,0)

vc = [0,0]
vfacing = UP
ic = 0
wc = 0
fc = 0
cc = 0

def move(v,d):
    return (v[0]+d[0],v[1]+d[1])

tR = {UP:RIGHT, RIGHT:DOWN, DOWN:LEFT, LEFT:UP}
tL = {UP:LEFT, LEFT:DOWN, DOWN:RIGHT, RIGHT:UP}
def turn_right(f):
    return tR[f]
def turn_left(f):
    return tL[f]
def opposite(f):
    return tR[tR[f]]

def burst():
    global grid
    global vc
    global vfacing
    global ic

    if grid[vc[0],vc[1]] == '#':
        vfacing = turn_right(vfacing)
    else:
        vfacing = turn_left(vfacing)
    if grid[vc[0],vc[1]] == '.':
        ic += 1
        grid[vc[0],vc[1]] = '#'
    else:
        grid[vc[0],vc[1]] = '.'
    vc = move(vc,vfacing)

def burst2():
    global grid
    global vc
    global vfacing
    global ic
    global wc
    global fc
    global cc

    if grid[vc[0],vc[1]] == '.':
        vfacing = turn_left(vfacing)
    elif grid[vc[0],vc[1]] == '#':
        vfacing = turn_right(vfacing)
    elif grid[vc[0],vc[1]] == 'F':
        vfacing = opposite(vfacing)
    
    if grid[vc[0],vc[1]] == '.':
        wc += 1
        grid[vc[0],vc[1]] = 'W'
    elif grid[vc[0],vc[1]] == 'W':
        ic += 1
        grid[vc[0],vc[1]] = '#'
    elif grid[vc[0],vc[1]] == '#':
        fc += 1
        grid[vc[0],vc[1]] = 'F'
    elif grid[vc[0],vc[1]] == 'F':
        cc += 1
        grid[vc[0],vc[1]] = '.'
    
    vc = move(vc,vfacing)

def print_grid(grid):
    gkeys = grid.keys()
    minx,miny = min(k[0] for k in gkeys),min(k[1] for k in gkeys)
    maxx,maxy = max(k[0] for k in gkeys),max(k[1] for k in gkeys)
    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            print(grid[(x,y)],end='')
        print('')

gsize = len(input)

# Part 1
# for r in range(len(input)):
#     for c in range(len(input[r])):
#         if input[r][c] == '#':
#             grid[(c,r)] = '#'
# vc = [gsize//2,gsize//2]
# #print_grid(grid)

# for b in range(10000):
#     burst()
# print('infect count:',ic)

# Part 2
for r in range(len(input)):
    for c in range(len(input[r])):
        if input[r][c] == '#':
            grid[(c,r)] = '#'
vc = [gsize//2,gsize//2]
print(vc)
print_grid(grid)

for b in range(10000000):
    burst2()
    #print('new grid after burst',b,' : ',vc)
    #print_grid(grid)

print('infect count:',ic)