#!/usr/bin/env python3

import re
import collections

input_lines = open('day7.txt','r').read().strip().split('\n')

towers = dict()
tower_parents = dict()
weights = dict()

for t in input_lines:
    parts = t.split(' -> ')
    m = re.match(r"(\w+) \((\d+)\)",parts[0])
    base = m.group(1)
    towers[base] = []
    weights[base] = int(m.group(2))
    if len(parts) == 2:
        for st in parts[1].split(', '):
            towers[base].append(st)
            tower_parents[st] = base

root = ''
for w in weights:
    if w not in tower_parents:
        root = w
        break

print(root)
print(weights)

odd_weights = dict()
correct_weights = dict()
def find_balance(root):
    sums = [weights[root]]
    if len(towers[root]) == 0:
        return sums
    sub_sums = []
    for t in towers[root]:
        sub_sums.append(sum(find_balance(t)))
    
    sub_weights = collections.defaultdict(list)
    for i,s in enumerate(sub_sums):
        sub_weights[s].append(i)
    
    correct_weight = 0
    odd_tower = ''
    for k,v in sub_weights.items():
        if len(v) == 1:
            odd_tower = towers[root][v[0]]
            odd_weights[odd_tower] = k
            print(f"tower {odd_tower} has odd weight {k}")
        else:
            correct_weight = k    
    if odd_tower:
        print(f"weight should be {correct_weight}")
        print(f"{odd_weights[odd_tower]} => {correct_weight}")
        print(f"{weights[odd_tower]} -> {weights[odd_tower]-(odd_weights[odd_tower]-correct_weight)}")
        correct_weights[odd_tower] = weights[odd_tower]-(odd_weights[odd_tower]-correct_weight)
    return sums + sub_sums

#print(find_balance(root))
find_balance(root)

print("odd weights: ",odd_weights)

print("correct wts: ",correct_weights)
print(min(correct_weights.items(),key=lambda x:x[1]))