#!/usr/bin/env python3

### Advent of Code - 2015 - Day 22

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

spells = dict()
spells['Magic Missle'] = { 'cost':53, 'dmg':4, 'hp':0, 'armor':0, 'turns':0, 'mana':0 }
spells['Drain'] = { 'cost':73, 'dmg':2, 'hp':2, 'armor':0, 'turns':0, 'mana':0 }
spells['Shield'] = { 'cost':113, 'dmg':0, 'hp':0, 'armor':7, 'turns':6, 'mana':0 }
spells['Poison'] = { 'cost':173, 'dmg':3, 'hp':0, 'armor':0, 'turns':6, 'mana':0 }
spells["Recharge"] = { 'cost':229, 'dmg':0, 'hp':0, 'armor':0, 'turns':5, 'mana':101 }

def take_turn(players_turn, boss_hp, player_hp, player_mana, active_spells, mana_used):
    if players_turn and p2:
        player_hp -= 1
        if player_hp <= 0:
            return

    player_armor = 0    
    new_spells = dict()
    for n,d in active_spells.items():
        if d['turns'] >= 0: # perform the spell this turn
            boss_hp -= d['dmg']
            player_hp += d['hp']
            player_armor += d['armor']
            player_mana += d['mana']
        new_sp = d.copy()
        new_sp['turns'] -= 1
        if new_sp['turns'] > 0:
            new_spells[n] = new_sp

    if boss_hp <= 0: # we win!
        global least_mana_used
        least_mana_used = min(mana_used, least_mana_used)
        return

    if mana_used >= least_mana_used:
        return

    if players_turn:
        for n,d in spells.items():
            if n in new_spells.keys(): # can't cast an already active spell
                continue
            if d['cost'] <= player_mana:
                nsp_copy = new_spells.copy()
                nsp_copy[n] = d.copy()
                take_turn(False, boss_hp, player_hp, player_mana-d['cost'], nsp_copy, mana_used+d['cost'])
    else:
        player_hp += player_armor-boss_dmg if player_armor-boss_dmg < 0 else -1
        if player_hp > 0:
            take_turn(True, boss_hp, player_hp, player_mana, new_spells, mana_used)
    return

# Setup
player_hp = 50
player_mana = 500
boss_hp = int(input_lines[0].split()[-1])
boss_dmg = int(input_lines[1].split()[-1])

p2 = False
least_mana_used = 9999999
take_turn(True, boss_hp, player_hp, player_mana, dict(), 0)
part1(least_mana_used)

p2 = True
least_mana_used = 9999999
take_turn(True, boss_hp, player_hp, player_mana, dict(), 0)
part2(least_mana_used)
