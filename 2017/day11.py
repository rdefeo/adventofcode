#!/usr/bin/env python3

import re
import functools

input = open('day11.txt','r').read().strip()

# Hex tiling algorithms - https://www.redblobgames.com/grids/hexagons/
# For this problem, we're using the odd-q tiling

dir = input
#dir = 'ne,ne,ne'
#dir = 'ne,ne,sw,sw'
#dir = 'ne,ne,s,s'
#dir = 'se,sw,se,sw,sw'
dir = dir.split(',')

move_to_odd = {
    'n' : lambda p: [p[0],p[1]-1],
    'ne': lambda p: [p[0]+1,p[1]],
    'se': lambda p: [p[0]+1,p[1]+1],
    's' : lambda p: [p[0],p[1]+1],
    'sw': lambda p: [p[0]-1,p[1]+1],
    'nw': lambda p: [p[0]-1,p[1]],
}
move_to_even = {
    'n' : lambda p: [p[0],p[1]-1],
    'ne': lambda p: [p[0]+1,p[1]-1],
    'se': lambda p: [p[0]+1,p[1]],
    's' : lambda p: [p[0],p[1]+1],
    'sw': lambda p: [p[0]-1,p[1]],
    'nw': lambda p: [p[0]-1,p[1]-1],
}
def move_to(d,pos):
    if pos[0]&1:
        return move_to_odd[d](pos)
    else:
        return move_to_even[d](pos)

def oddq_to_cube(p):
    x = p[0]
    z = p[1] - (p[0] - (p[0]&1)) // 2
    y = -x - z
    return (x,y,z)

def cube_to_oddq(c):
    x = c[0]
    y = c[2] + (c[0] - (c[0]&1)) // 2
    return (x,y)

def cube_distance(a,b):
    return max(abs(a[0]-b[0]),abs(a[1]-b[1]),abs(a[2]-b[2]))

def distance(a,b):
    ac = oddq_to_cube(a)
    bc = oddq_to_cube(b)
    return cube_distance(ac,bc)

origin = [0,0]
pos = origin
max_dist = 0
for d in dir:
    pos = move_to(d,pos)
    max_dist = max(max_dist,distance(origin,pos))

print("Part 1: ",distance(origin,pos))

print("Part 2: ",max_dist)