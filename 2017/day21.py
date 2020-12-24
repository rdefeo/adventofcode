#!/usr/bin/env python3


import re
import sys
import collections

infile = 'day21.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().split('\n')


start = ['.#.','..#','###']

rules = dict()

def part(a):
    for y in a:
        print(''.join(y))

def pluck_piece(a,x,y,s):
    p = []
    for py in range(y,y+s):
        p.append(a[py][x:x+s])
    return p

def create_art(a):
    step = 2 if len(a) % 2 == 0 else 3
    nstep = step+1
    na = ['']*(len(a)//step * nstep)
    ny = 0
    #print('step:',step,'nstep:',nstep,'ns:',ns,'len a',len(a))
    for y in range(0,len(a),step):
        nx = 0
        for x in range(0,len(a),step):
            p = pluck_piece(a,x,y,step)
            #print('plucked:',p,"at:",x,y)
            pf = '/'.join(p)
            if pf in rules:
                pe = rules[pf].split('/')
                for r,e in enumerate(pe):
                    na[ny+r] += e
                #print('matched enh:',pe)
            else:
                print("uh... now what")
                quit()
            nx += nstep
        ny += nstep
    return na

print("> Reading Rules:")
for l in input:
    r,e = l.split(' => ')[0].split('/'),l.split(' => ')[1]
    s = len(r)
    # find all permutations of the rule (rotate/mirror/etc)
    
    print(r)
    rules['/'.join(r)] = e
    rules['/'.join(r[::-1])] = e
    rules['/'.join([x[::-1] for x in r])] = e
    rules['/'.join([x[::-1] for x in r[::-1]])] = e

    # Transpose, then flip
    t = list(map(list,zip(*r)))
    rt = [''.join(x) for x in t]
    
    rules['/'.join(rt)] = e
    rules['/'.join(rt[::-1])] = e
    rules['/'.join([x[::-1] for x in rt])] = e
    rules['/'.join([x[::-1] for x in rt[::-1]])] = e
print("< Done with Rules")

def create_art_loop(art,loop):
    for i in range(loop):
        nart = create_art(art)
        #print(f"new art [{i}]:")
        #part(nart)
        art = nart
    return art

print("Part 1:")
print(sum(x.count('#') for x in create_art_loop(start,5)))

print("Part 2:")
print(sum(x.count('#') for x in create_art_loop(start,18)))