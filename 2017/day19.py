#!/usr/bin/env python3

import collections
import sys

infile = 'day19.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().split('\n')

UP = (0,-1)
RIGHT = (1,0)
DOWN = (0,1)
LEFT = (-1,0)

pos = []
facing = DOWN

oppd = {UP:DOWN,RIGHT:LEFT,DOWN:UP,LEFT:RIGHT}

move_count = 1
moves = []
def move(p,f):
    #print("moving from",p,"to",f)
    return [p[0]+f[0],p[1]+f[1]]

def get(pos):
    return input[pos[1]][pos[0]]

def pget(p,d):
    nx,ny = p[0]+d[0],p[1]+d[1]
    if 0 <= ny < len(input) and 0 <= nx < len(input[ny]):
        return input[ny][nx]
    return None

def get_turn(p,f):
    alld = [UP,RIGHT,DOWN,LEFT]
    for a in alld:
        if a == oppd[f]:
            continue
        peek = pget(p,a)
        if peek and peek != ' ':
            return a
    print('No turn found?')
    return None

letters = ''

# find the start
print(input[0])
for i,p in enumerate(input[0]):
    if p == '|':
        pos = [i,0]
        break
print("starting pos:",pos)
for l in input:
    print(l)

crossing = False

while True:
    
    move_count += 1
    pos = move(pos,facing)
    g = get(pos)
    if g.isalpha():
        letters += g
        print("found",g)
        if g == 'S' or g == 'F':
            print(letters)
            moves.append(move_count)
            print(moves)
            print(sum(moves))
            quit()
        continue # keep going in same direction
    elif g == '|':
        if facing == DOWN or facing == UP:
            continue
        elif facing == RIGHT or facing == LEFT:
            crossing = True # keep dir same
            continue
    elif g == '-':
        if facing == RIGHT or facing == LEFT:
            continue
        elif facing == DOWN or facing == UP:
            crossing = True
            continue
    elif g == '+':
        # need to turn, but where?
        ndir = get_turn(pos,facing)
        moves.append(move_count)
        move_count = 0
        if ndir:
            #print("new dir is",ndir)
            facing = ndir
        else:
            print("at end of route")
            print(letters)
            print(moves)
            print(move_count)
            quit()

