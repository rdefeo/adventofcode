#!/usr/bin/env python3

### Advent of Code - 2021 - Day 23

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq

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

# Store the location of every amphipod, along with their state. All pods start in a room,
# must visit the hallway, and then go back to their own room. (Some pods may already start
# in their room - we should special case this. Right now, the test cases fail bu tthe real
# inputs work - yay)
# e.g. [ ('A',(3,2),START), ... ]
pods = []
START, HALL, ROOM = 0, 1, 2
for y, line in enumerate(finput.split('\n')):
    for x, l in enumerate(line):
        if l in 'ABCD':
            pods.append((l,(x,y),START))

# Allow for a variable room depth to handle Part 1 and Part 2 inputs
ROOM_DEPTH = len(input_lines)-3

# Map of all rooms to their positions
room = {r:[(x,i) for i in range(2,2+ROOM_DEPTH)] for r,x in zip('ABCD',[3,5,7,9]) }
roomX = {'A':3,'B':5,'C':7,'D':9}

# Amphipod movement energy cost
COST = {'A':1, 'B':10, 'C':100, 'D':1000}

# Given the current list of all pods, p, and one specific pod, pod, generate the list
# of all possible moves. 
def gen_possible_moves(p,pod):
    name,pos,state = pod
    no_move = []
    if state == ROOM: return no_move # you're already in your room, yay!
    if state == HALL:
        # only possible move is into our assigned room, if no one is blocking progress
        
        # are there pods in our room that haven't yet moved from their starting position?
        pods_in_our_room = {s for s in p if s[2] == START and s[1] in room[name]}
        if pods_in_our_room:
            return no_move
        
        # setup our hallway range, based on whether we need to go left or right
        hrange = range(pos[0]+1,roomX[name]+1)
        if pos[0] > roomX[name]:
            hrange = range(pos[0]-1,roomX[name]-1,-1)

        # are there any other pods in the hallway between us and our room?
        if not any((i,1) in {h[1] for h in p if h[2] == HALL} for i in hrange):
            steps = abs(roomX[name] - pos[0])
            # how far into room can we go?
            us_in_room = {u for u in p if u[0] == name and u[2] == ROOM}
            steps += (ROOM_DEPTH-len(us_in_room))
            dest = (roomX[name],(ROOM_DEPTH+1)-len(us_in_room))
            return [(ROOM,dest,steps*COST[name])]
        return no_move

    else: # START, we're in a starting room
        # only possible moves are into the hallway directly to our room, if no one is blocking
        # if we're in a room, and there's someone above us, no moves
        if any(s[1][1]<pos[1] for s in p if s[2] == START and s[1][0] == pos[0]):
            return no_move
        
        # need to handle the case where we're starting in our own room and don't need to move!
        if pos in room[name]:
            pods_below_us = [s for s in room[name] if s[1] > pos[1]]
            if not pods_below_us or all(s[0]==name and s[2]==ROOM for s in pods_below_us):
                return [(ROOM,pos,0)] # this effectively sets our state from START to ROOM

        possible = []
        us_in_room = {u for u in p if u[0] == name and u[2] == ROOM}
        pods_in_hall = {h[1] for h in p if h[2] == HALL}

        steps = pos[1]-1 # steps to get out of room
        for x in range(pos[0]+1,12): # try going right down hall
            if (x,1) in pods_in_hall:
                break
            steps += 1
            if x not in [3,5,7,9]:
                possible.append((HALL,(x,1),steps*COST[name]))
            if x == roomX[name]: # reached our room, can we go in?
                if any([u[1][0]==x for u in p if u != pod and u[2] == START]):
                    continue # no, others are still there
                steps += ROOM_DEPTH-len(us_in_room)
                return [(ROOM,(roomX[name],3-len(us_in_room)),steps*COST[name])]
        
        steps = pos[1]-1 # steps to get out of room
        for x in range(pos[0]-1,0,-1): # try going left down hall
            if (x,1) in pods_in_hall:
                break
            steps += 1
            if x not in [3,5,7,9]:
                possible.append((HALL,(x,1),steps*COST[name]))
            if x == roomX[name]: # reached our room, can we go in?
                if any([u[1][0]==x for u in p if u != pod and u[2] == START]):
                    continue # no, others are still there
                steps += ROOM_DEPTH-len(us_in_room)
                return [(ROOM,(roomX[name],3-len(us_in_room)),steps*COST[name])]

        return possible
    
# BFS solution - for every state (the pods list), try moving every pod to every
# possible location. By using a heap, we ensure a minimum energy cost
def solve(p):
    q = [ (0, tuple(p), []) ] # energy, pods, solution steps
    seen = set()
    while q:
        energy, curr, steps = heapq.heappop(q)
        if curr not in seen:
            seen.add(curr)
            if all(i[2]==ROOM for i in curr):
                print(f"all pods are in their rooms! {energy=}")
                for s in steps:
                    print(s)    
                return energy
            for i,pod in enumerate(curr):
                for loc,dest,eng in gen_possible_moves(curr,pod):
                    new_pods = list(curr)
                    new_pods[i] = (pod[0],dest,loc)
                    heapq.heappush(q, (energy+eng, tuple(new_pods), tuple(list(steps)+[(pod[0],pod[1],dest,eng)])))
    return float("inf")

part1(solve(pods))

