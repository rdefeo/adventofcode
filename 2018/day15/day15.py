#!/usr/bin/env python3

### Advent of Code - 2018 - Day 15

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import copy

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


class Unit():
    def __init__(self,t,pos):
        self.type = t # 'E' or 'G'
        self.pos = pos # Y,X tuple
        self.hp = 200
        self.attack = 3
        self.alive = True
    def __repr__(self):
        return f"{self.type}: {self.pos} / {self.hp}:{self.attack}"
    def move(self):
        pass
    def attack(self):
        pass


def print_cave(cave):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(cave[(y,x)],end='')
        print('')

def sort_units(units):
    return sorted(units,key=lambda u:u.pos)

def find_targets(unit,units):
    return sort_units([tgt for tgt in units if unit.type != tgt.type and tgt.alive])

def neighbors(pos):
    directions = [(1,0),(0,1),(-1,0),(0,-1)] # D,R,U,L
    return [(pos[0]+d[0],pos[1]+d[1]) for d in directions]

def find_open_spaces(unit,cave):
    return [sp for sp in neighbors(unit.pos) if cave[sp] == '.']

def find_enemies_in_range(unit,units):
    enemies = []
    n = neighbors(unit.pos)
    for t in units:
        if t.type != unit.type and t.pos in n and t.alive:
            enemies.append(t)
    return sorted(enemies,key=lambda u:(u.hp,u.pos))

# Breadth First Search from the unit position to every other space
# in the cave. Along the way, store the distance from each visited
# square to the next, recording how we got there
def find_best_move(unit,units,open_spaces,cave):
    visiting = [(unit.pos,0)] # list of positions,dist we need to visit
    distances = {unit.pos:(0,None)} # keep track of distances calculated
    seen = set()
    occupied = {u.pos for u in units if u.alive}

    while visiting:
        pos,dist = visiting.pop(0)
        for n in neighbors(pos):
            if cave[n] == '#' or n in occupied:
                continue
            # either, we haven't been here before,
            # or we got here previously but took a longer path
            if n not in distances or distances[n] > (dist+1,pos):
                distances[n] = (dist+1,pos)
            if n in seen:
                continue
            # add our neighbors to our list of squares to visit, if they're
            # not already in our visiting list
            if not any(n==v[0] for v in visiting):
                visiting.append((n,dist+1))
        seen.add(pos)

    # for ever square recorded in distances, find the one that has the shortest
    # recorded distance - and only concern ourselves with squares that are in our
    # open_spaces list. this is the closest open space.
    open_space_distances = [(dist,pos) for pos,(dist,_) in distances.items() if pos in open_spaces]

    # it's possible that we can't move anywhere, and/or find a path to any
    # of the open spaces
    closest_pos = None
    if open_space_distances:
        _,closest_pos = min(open_space_distances)
    else:
        return
    # Now that we found the closest open space, lookup how we got there, and keep
    # doing so until the recorded distance is 1. we now know the first step from
    # the source unit we must take
    while distances[closest_pos][0] > 1:
        closest_pos = distances[closest_pos][1]
    return closest_pos

orig_cave = collections.defaultdict(lambda:'.')
orig_units = []

WIDTH = len(input_lines[0])
HEIGHT = len(input_lines)
for y,l in enumerate(input_lines):
    for x,c in enumerate(l):
        if c in 'GE':
            orig_units.append(Unit(c,(y,x)))
        orig_cave[(y,x)] = c

print("Initially:")
print_cave(orig_cave)

def set_elf_power(power):
    units = copy.deepcopy(orig_units)
    for u in units:
        if u.type == 'E':
            u.attack = power
    return units

def simulate_combat(epower=3,part2=False):
    rounds = 0
    can_move = True
    cave = orig_cave.copy()
    units = set_elf_power(epower)
    print(units)
    while can_move:
        print("Round:",rounds+1)
        targets_to_attack = True
        for u in sort_units(units):
            if not u.alive: continue

            # identify enemy targets, if no enemies, combat ends
            targets = find_targets(u,units)
            #print("Targets:",targets)
            if not targets:
                targets_to_attack = False
                break
            
            # if any of the targets are within range, we don't need to move
            enemies = find_enemies_in_range(u,units)
            if not enemies:
                # identify open square in range of each target
                open_spaces = []
                for tgt in targets:
                    open_spaces += find_open_spaces(tgt,cave)
                
                move = find_best_move(u,units,open_spaces,cave)
                if move:
                    # print(f"Best move for {u.pos} is {move}")
                    cave[u.pos] = '.'
                    u.pos = move
                    cave[u.pos] = u.type
            
            enemies = find_enemies_in_range(u,units)
            if enemies:
                e = enemies[0]
                e.hp -= u.attack
                if e.hp <= 0:
                    e.alive = False
                    cave[e.pos] = '.'
                    if part2 and e.type == 'E':
                        print("ELF DIED! Aborting combat!")
                        return None

                
        print([u for u in sort_units(units) if u.alive])
        print_cave(cave)
            
        rounds += 1 # we made it a full round!

        if not targets_to_attack:
            # we're done with combat, compute score
            print("No targets remaining. Ending combat.")
            rounds -= 1
            break

    print(f"Game over: Rounds: {rounds}")

    print("Still alive:",[u.hp for u in units if u.alive])
    return rounds * sum(u.hp for u in units if u.alive) 

result = simulate_combat(3)
if result:
    part1(result)
quit()
power = 3
elves_lose = True
while elves_lose:
    power += 1
    result = simulate_combat(power,True)
    if result:
        elves_lose = False
print("Elf power required",power)
part2(result)