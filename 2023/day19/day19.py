#!/usr/bin/env python3

### Advent of Code - 2023 - Day 19

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

data1, data2 = finput.split('\n\n')

class Rule:
    def __init__(self,code):
        # e.g. code = 'a<2006:qkq'  or code = 'rfg'
        tokens = code.split(':')
        self.var = None
        if len(tokens) == 1:
            self.next_wflow = tokens[0]
        else:
            self.var = tokens[0][0]
            self.op = tokens[0][1]
            self.val = int(tokens[0][2:])
            self.next_wflow = tokens[1]
    def passes(self,part):
        if not self.var: # this is an end rule, no eval necessary
            return True
        return eval(str(part[self.var]) + self.op + str(self.val))

# For each workflow, parse and store the list of rules
workflows = collections.defaultdict(list)
for line in data1.split():
    # e.g. line = 'px{a<2006:qkq,m>2090:A,rfg}'
    name, rest = line.split('{')
    rules = rest[:-1].split(',')
    for r in rules:
        workflows[name].append(Rule(r))

# Part 1
# For every part, start at 'in' and evaluate each rule. Jump to the
# next location if our part passes the rule. Otherwise, keep processing
# the rules of that workflow. If our final workflow ends in acceptance ('A')
# then accumulate our part values
accepted_rating = 0
for line in data2.split():
    p = { m[0]: int(m[1]) for m in re.findall(r"([xmas])=(\d+)",line) }
    wflow = 'in'
    while wflow not in 'AR':
        for r in workflows[wflow]:
            if not r.passes(p):
                continue
            wflow = r.next_wflow
            break
    if wflow == 'A':
        accepted_rating += sum(p.values())
part1(accepted_rating)

# Part 2
# All parts had their specs store in vars x, m, a, s, in that order. Create a
# new part that's actually a range of spec values. Then evaluate those ranges
# against the same workflow/rules as before. In some cases all values of a range
# are good, sometimes not. And in some cases, half the range passes (which takes
# us to our next workflow) and the other half fails (which takes us to our next
# rule). At the end, accumulate the product of spec value ranges
parts = [ ('in', [1, 4000, 1, 4000, 1, 4000, 1, 4000]) ]
total_combs = 0
while parts:
    wflow, part = parts.pop(0)

    if wflow == 'A':
        # our part was accepted! compute the combinations and accumulate
        combs = 1
        for i in range(0,len(part),2):
            combs *= (part[i+1]-part[i]+1)
        total_combs += combs    
        continue

    # For this part, eval the rules of the current workflow
    for r in workflows[wflow]:
        # Is this the last rule?
        if not r.var: # no variable means just go to the next workflow
            parts.append( (r.next_wflow, part.copy()) )
            break

        # which variable index is this rule for?
        vi = 'xmas'.find(r.var) * 2
        lo, hi = part[vi:vi+2] # rule range for this var

        # Should we be less than the rule val? If so, then we have 3 options:
        #   val < lo < hi - entire range fails rule, move to next rule
        #   lo < val < hi - 1st half passes, 2nd half fails so create
        #                   two parts and move to next workflow or next rule
        #   lo < hi < val - entire range passes, move to next workflow
        if r.op == '<':
            if r.val <= lo: # entire range fails, next rule
                continue
            if r.val <= hi: # split range!
                # 1st half succeeds, go to next dest
                # 2nd half fails, continue to next rule
                part[vi] = lo
                part[vi+1] = r.val-1
                parts.append( (r.next_wflow, part.copy()) )
                part[vi] = r.val
                part[vi+1] = hi
                continue
            if hi < r.val: # entire range passes!, next dest
                parts.append( (r.next_wflow, part.copy()) )
                break
        # Similar to above, but reversed
        if r.op == '>':
            if r.val >= hi: # entire range fails, next rule
                continue
            if r.val >= lo: # split range!
                part[vi] = r.val+1
                part[vi+1] = hi
                parts.append( (r.next_wflow, part.copy()) )
                part[vi] = lo
                part[vi+1] = r.val
                continue
            if lo > r.val:
                parts.append( (r.next_wflow, part.copy()) )
                break
                
part2(total_combs)

