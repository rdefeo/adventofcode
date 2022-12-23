#!/usr/bin/env python3

### Advent of Code - 2022 - Day 22

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# Read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
finput = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in finput.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


# Read the input grid
field, password = finput.split('\n\n')
field = field.split('\n')

grid = collections.defaultdict(lambda:' ')
sloc = None # starting location
for y, line in enumerate(field):
    for x, g in enumerate(line):
        grid[(x,y)] = g
        if g != ' ' and not sloc:
            sloc = (x,y)
max_x = max([len(line) for line in field])
max_y = len(field)

# Parse the input steps/password
steps = re.findall(r'\d+|[LR]',password)

# Print grid for debugging. If we pass in our 'track', print it too
def print_grid(t=None):
    for y in range(max_y):
        for x in range(max_x):
            if t and (x,y) in t:
                print(t[(x,y)],end='')
            else:
                print(grid[(x,y)],end='')
        print()
    print()

RIGHT, DOWN, LEFT, UP = (1,0), (0,1), (-1,0), (0,-1)
turn_right = { RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT }
turn_left  = { RIGHT: UP, UP: LEFT, LEFT: DOWN, DOWN: RIGHT }
turn = { 'R': turn_right, 'L': turn_left }
marker = { RIGHT: '>', DOWN: 'v', LEFT: '<', UP: '^' }
fscore = { RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3 }

# Define the face connections for Part 2
# All 50x50 faces fall within their own "face coordinates". After we manually
# determined how our cube folded, we know that a move from face (1,1) to face
# (0,2) [which means we're moving left] will result in us then moving down.
# So we just used pencil and paper to determine each face-edge pair, which is
# our key in the faces dict. This maps to the new facing direction and a lambda
# which will put us from one edge to the next.
faces = dict()
fsize = 50
faces[((1,0),(1,-1))] = (RIGHT, lambda x: (0,3*fsize+(x[0]-fsize)))
faces[((0,3),(-1,3))] = (DOWN, lambda x: (fsize+(x[1]-3*fsize),0))

faces[((1,0),(0,0))] = (RIGHT, lambda x: (0,3*fsize-1-x[1]))
faces[((0,2),(-1,2))] = (RIGHT, lambda x: (fsize,3*fsize-1-x[1]))

faces[((1,1),(0,1))] = (DOWN, lambda x: (x[1]-fsize,2*fsize))
faces[((0,2),(0,1))] = (RIGHT, lambda x: (fsize,fsize+x[0]))

faces[((1,1),(2,1))] = (UP, lambda x: (2*fsize+(x[1]-fsize),fsize-1))
faces[((2,0),(2,1))] = (LEFT, lambda x: (2*fsize-1,fsize+(x[0]-2*fsize)))

faces[((0,3),(1,3))] = (UP, lambda x: (fsize+(x[1]-3*fsize),3*fsize-1))
faces[((1,2),(1,3))] = (LEFT, lambda x: (fsize-1,3*fsize+(x[0]-fsize)))

faces[((1,2),(2,2))] = (LEFT, lambda x: (3*fsize-1,3*fsize-1-x[1]))
faces[((2,0),(3,0))] = (LEFT, lambda x: (2*fsize-1,3*fsize-1-x[1]))

faces[((2,0),(2,-1))] = (UP, lambda x: (x[0]-2*fsize,4*fsize-1))
faces[((0,3),(0,4))] = (DOWN, lambda x: (2*fsize+x[0],0))

# The core of the problem: how we move forward, given the wrapping rules of each part
def move_forward(m, f, p):
    new_me = (m[0]+f[0],m[1]+f[1])
    if p == 1:
        # basic rectangular wrapping
        if grid[new_me] == ' ': # we're walking off the map! wrap around
            nl = { RIGHT: (0,m[1]), DOWN: (m[0],0), LEFT: (max_x-1,m[1]), UP: (m[0],max_y-1) }[f]
            while grid[nl] == ' ': # if we ended up in empty space after wrapping, keep moving
                nl = (nl[0]+f[0],nl[1]+f[1])
            if grid[nl] != '#': # only assign our new location if we didn't hit a rock!
                m = nl
        elif grid[new_me] != '#':
            m = new_me
    else:
        # which face are we in? and if we attempt a step forward, is it in a new face?
        # if so, check if we need to relocate our coordinates and update our facing dir
        curr_face = (m[0]//fsize, m[1]//fsize) # map our loc to face coordinates
        next_face = (new_me[0]//fsize, new_me[1]//fsize)
        if (curr_face,next_face) in faces:
            nfacing, warp_fn = faces[(curr_face,next_face)]
            new_me = warp_fn(m)
            if grid[new_me] != '#':
                return new_me, nfacing
            else:
                return m, f
        elif grid[new_me] != '#':
           m = new_me
    return m, f

# Follow the password instructions and move and turn and move and turn ...
def trace_path(me, facing, part):
    track = dict()  
    for s in steps:
        if s in 'LR':
            facing = turn[s][facing]
            track[(me)] = marker[facing]
        else:
            for _ in range(int(s)):
                track[(me)] = marker[facing]
                me, facing = move_forward(me,facing,part)
    return me, facing, track

me, facing, track = trace_path(sloc, (1,0), 1)
# print_grid(track)
print(me)
part1(1000 * (me[1]+1) + 4 * (me[0]+1) + fscore[facing])

# Part 2
# This part required us folding out cube manually and defining the translation
# states between non-adjacent faces (see above). Paper cube to the rescue!
me, facing, track = trace_path(sloc, (1,0), 2)
# print_grid(track)
print(me)
part2(1000 * (me[1]+1) + 4 * (me[0]+1) + fscore[facing])
