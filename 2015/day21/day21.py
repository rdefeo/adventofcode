#!/usr/bin/env python3

### Advent of Code - 2015 - Day 21

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

class Item():
    def __init__(self, gold = 0, damage = 0, armor = 0):
        self.gold = gold
        self.damage = damage
        self.armor = armor

weapons = [Item(8, 4, 0), Item(10, 5, 0), Item(25, 6, 0), Item(40, 7, 0), Item(74, 8, 0)]
armor = [Item(13, 0, 1), Item(31, 0, 2), Item(53, 0, 3), Item(75, 0, 4), Item(102, 0, 5)]
rings = [Item(25, 1, 0), Item(50, 2, 0), Item(100, 3, 0), Item(20, 0, 1), Item(40, 0, 2), Item(80, 0, 3)]

def total(x, stat):
    if hasattr(x, stat):
        return getattr(x, stat)
    return sum(getattr(y, stat) for y in x)

def fight(w, a, r):
    b_hp, b_dmg, b_arm = 100, 8, 2 # our boss
    hp = 100
    while True:
        dmg = (total(w, 'damage') + total(r, 'damage')) - b_arm
        b_hp -= max(dmg, 1)
        if b_hp <= 0:
            break
        dmg = b_dmg - (total(a, 'armor') + total(r, 'armor'))
        hp -= max(dmg, 1)
        if hp <= 0:
            break
    if hp > 0:
        return True
    return False

min_gold = 100000000
max_gold = 0
# Choose one weapon
for w in weapons:
    # Choose no armor (0,0,0), or one armor
    for a in [Item()] + armor:
        # Choose no ring (0,0,0), one ring, or any two rings
        for r in [Item()] + rings + list(itertools.combinations(rings, 2)):
            gold = total(w, 'gold') + total(a, 'gold') + total(r, 'gold')
            if fight(w, a, r):
                min_gold = min(gold, min_gold)
            else:
                max_gold = max(gold, max_gold)
part1(min_gold)
part2(max_gold)
