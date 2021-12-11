#!/usr/bin/env python3

### Advent of Code - 2018 - Day 24

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from copy import deepcopy

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

# test1 inputs
groups = [
    {'army':'immune', 'n':1, 'units':17, 'hp':5390, 'weak':['radiation','bludgeoning'], 'immune':[], 'attack':4507, 'atype':'fire', 'initiative':2, 'selected':False },
    {'army':'immune', 'n':2, 'units':989, 'hp':1274, 'weak':['bludgeoning','slashing'], 'immune':['fire'], 'attack':25, 'atype':'slashing', 'initiative':3, 'selected':False },
    {'army':'infection', 'n':1, 'units':801, 'hp':4706, 'weak':['radiation'], 'immune':[], 'attack':116, 'atype':'bludgeoning', 'initiative':1, 'selected':False },
    {'army':'infection', 'n':2, 'units':4485, 'hp':2961, 'weak':['fire','cold'], 'immune':['radiation'], 'attack':12, 'atype':'slashing', 'initiative':4, 'selected':False }
]

groups = [
    {'army':'immune', 'n':1, 'units':1514, 'hp':8968, 'weak':['cold'], 'immune':[], 'attack':57, 'atype':'bludgeoning', 'initiative':9, 'selected':False },
    {'army':'immune', 'n':2, 'units':2721, 'hp':6691, 'weak':['cold'], 'immune':[], 'attack':22, 'atype':'slashing', 'initiative':15, 'selected':False },
    {'army':'immune', 'n':3, 'units':1214, 'hp':10379, 'weak':[], 'immune':['bludgeoning'], 'attack':69, 'atype':'fire', 'initiative':16, 'selected':False },
    {'army':'immune', 'n':4, 'units':2870, 'hp':4212, 'weak':[], 'immune':[], 'attack':11, 'atype':'radiation', 'initiative':12, 'selected':False },
    {'army':'immune', 'n':5, 'units':1239, 'hp':5405, 'weak':['cold'], 'immune':[], 'attack':37, 'atype':'cold', 'initiative':18, 'selected':False },
    {'army':'immune', 'n':6, 'units':4509, 'hp':4004, 'weak':['cold'], 'immune':['radiation'], 'attack':8, 'atype':'slashing', 'initiative':20, 'selected':False },
    {'army':'immune', 'n':7, 'units':3369, 'hp':10672, 'weak':['slashing'], 'immune':[], 'attack':29, 'atype':'cold', 'initiative':11, 'selected':False },
    {'army':'immune', 'n':8, 'units':2890, 'hp':11418, 'weak':['fire'], 'immune':['bludgeoning'], 'attack':30, 'atype':'cold', 'initiative':8, 'selected':False },
    {'army':'immune', 'n':9, 'units':149, 'hp':7022, 'weak':['slashing'], 'immune':[], 'attack':393, 'atype':'radiation', 'initiative':13, 'selected':False },
    {'army':'immune', 'n':10, 'units':2080, 'hp':5786, 'weak':['fire'], 'immune':['slashing','bludgeoning'], 'attack':20, 'atype':'fire', 'initiative':7, 'selected':False },

    {'army':'infection', 'n':1, 'units':817, 'hp':47082, 'weak':[], 'immune':['slashing','radiation','bludgeoning'], 'attack':115, 'atype':'cold', 'initiative':3, 'selected':False },
    {'army':'infection', 'n':2, 'units':4183, 'hp':35892, 'weak':[], 'immune':[], 'attack':16, 'atype':'bludgeoning', 'initiative':1, 'selected':False },
    {'army':'infection', 'n':3, 'units':7006, 'hp':11084, 'weak':[], 'immune':[], 'attack':2, 'atype':'fire', 'initiative':2, 'selected':False },
    {'army':'infection', 'n':4, 'units':4804, 'hp':25411, 'weak':[], 'immune':[], 'attack':10, 'atype':'cold', 'initiative':14, 'selected':False },
    {'army':'infection', 'n':5, 'units':6262, 'hp':28952, 'weak':['fire'], 'immune':[], 'attack':7, 'atype':'slashing', 'initiative':10, 'selected':False },
    {'army':'infection', 'n':6, 'units':628, 'hp':32906, 'weak':['slashing'], 'immune':[], 'attack':99, 'atype':'radiation', 'initiative':4, 'selected':False },
    {'army':'infection', 'n':7, 'units':5239, 'hp':46047, 'weak':[], 'immune':['fire'], 'attack':14, 'atype':'bludgeoning', 'initiative':6, 'selected':False },
    {'army':'infection', 'n':8, 'units':1173, 'hp':32300, 'weak':['cold','slashing'], 'immune':[], 'attack':53, 'atype':'bludgeoning', 'initiative':19, 'selected':False },
    {'army':'infection', 'n':9, 'units':3712, 'hp':12148, 'weak':['slashing'], 'immune':['cold'], 'attack':5, 'atype':'slashing', 'initiative':17, 'selected':False },
    {'army':'infection', 'n':10, 'units':334, 'hp':43582, 'weak':['cold','fire'], 'immune':[], 'attack':260, 'atype':'cold', 'initiative':5, 'selected':False }
]
print(groups)

def power(group):
    if group['units'] > 0:
        return group['units'] * group['attack']
    return 0

def calculate_damage(attacker,defender):
    damage = 0
    # print(type(attacker),type(defender))
    if attacker['atype'] in defender['weak']:
        damage = power(attacker) * 2
    elif attacker['atype'] not in defender['immune']:
        damage = power(attacker)
    return damage

def select_target(group,groups):
    max_damage = 0
    selected = None
    for g in groups:
        if g['selected'] or g == group or g['units'] <= 0 or g['army'] == group['army']:
            continue
        # compute how much damage (group) can do to (g)
        damage = calculate_damage(group,g)
        if damage > max_damage:
            selected = g
            max_damage = damage
        elif damage == max_damage and selected:
            if power(g) > power(selected):
                selected = g
            elif power(g) == power(selected):
                if g['initiative'] > selected['initiative']:
                    selected = g
    if not selected:
        return None
    selected['selected'] = True
    return selected

def select_targets(groups):
    selected = []
    # reset selected flags
    for g in groups:
        g['selected'] = False

    # print('selecting:')
    for group in sorted(groups,reverse=True,key=lambda x:(power(x),x['initiative'])):
        # print(' >',group['army'],group['n'],power(group),group['initiative'])
        if group['units'] == 0:
            continue
        target = select_target(group,groups)
        if target:
            selected.append((group,target))
    return selected

def fight():
    # for each group, select a target. (attacker, defender)
    targets = select_targets(groups)
    # for each group, attack it's selected target
    # print("Selected targets: ",targets)
    deaths = 0
    for (attacker,defender) in sorted(targets,reverse=True,key=lambda x:x[0]['initiative']):
        if attacker['units'] <= 0:
            continue
        # print(type(attacker),type(defender))
        damage = calculate_damage(attacker,defender)
        units_killed = math.floor(damage / defender['hp'])
        deaths += units_killed
        # actual_killed = defender['units'] if units_killed>defender['units'] else units_killed
        defender['units'] = max(0,defender['units']-units_killed)
        # print(attacker['army'],attacker['n'],'attacks ',end='')
        # print(defender['army'],defender['n'],', killing',actual_killed,'units')
    return deaths

def unit_count(army,groups):
    units = 0
    for g in groups:
        if g['army'] == army and g['units'] > 0:
            units += g['units']
    return units

part_2 = True
if not part_2:
    for g in groups:
        if g['army'] == 'immune':
            g['attack'] += 1570

boost = 1
immune_wins = False
orig_groups = deepcopy(groups)
while not immune_wins:
    groups = deepcopy(orig_groups)
    for g in groups:
        if g['army'] == 'immune':
            g['attack'] += boost
    while unit_count('immune',groups) and unit_count('infection',groups):
        # if boost == 81:
        #     print("Immune System:")
        #     for i in groups:
        #         if i['army'] == 'immune' and i['units'] > 0:
        #             print('Group',i['n'],'contains',i['units'],'units')
        #     print("Infection System:")
        #     for i in groups:
        #         if i['army'] == 'infection' and i['units'] > 0:
        #             print('Group',i['n'],'contains',i['units'],'units')
        #     print('')
        if not fight():
            print("No deaths occurred! boost:",boost)
            break
        # print('')
    if unit_count('immune',groups) and not unit_count('infection',groups):
        immune_wins = True
        part2("Immune WON with boost "+str(boost))
        break
    else:
        print("Immune lost with boost",boost)
    boost += 1
# print(groups)

part1("Immune System: "+str(unit_count('immune',groups)))
part1("Infection: "+str(unit_count('infection',groups)))