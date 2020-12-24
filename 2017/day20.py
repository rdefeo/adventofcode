#!/usr/bin/env python3

import re
import sys
import collections

infile = 'day20.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().split('\n')

class Particle:
    def __init__(self,id,p,v,a):
        self.id = id
        self.p = list(map(int,p))
        self.v = list(map(int,v))
        self.a = list(map(int,a))
        self.mdist = sum(map(abs,self.p))
    def __repr__(self):
        return 'p:'+','.join(list(map(str,self.p)))+' v:'+','.join(list(map(str,self.v)))+' a:'+','.join(list(map(str,self.a)))+' d:'+str(self.mdist)
    def update(self):
        self.v[0] += self.a[0]
        self.v[1] += self.a[1]
        self.v[2] += self.a[2]
        self.p[0] += self.v[0]
        self.p[1] += self.v[1]
        self.p[2] += self.v[2]
        self.mdist = sum(map(abs,self.p))

particles = []
for i,p in enumerate(input):
    m = re.findall(r"(-?\d+)",p)
    particles.append(Particle(i,m[0:3],m[3:6],m[6:9]))
#    print(particles[-1])
print(len(particles))

print("Part 1")
for t in range(600):
    for p in particles:
        p.update()
    if t % 500 == 0:
        parts = sorted(particles,key=lambda p:p.mdist)
        print(parts[0].id,parts[0].mdist)
        
particles = []
for i,p in enumerate(input):
    m = re.findall(r"(-?\d+)",p)
    particles.append(Particle(i,m[0:3],m[3:6],m[6:9]))

print("Part 2")
for t in range(5000):
    positions = collections.defaultdict(list)
    for i,p in enumerate(particles):
        p.update()
        # make the x,y,z position a hashable value
        positions[''.join(map(str,p.p))].append(p.id)

    for v in positions.values():
        if len(v) > 1:
            for pid in v:
                for i,p in enumerate(particles):
                    if pid == p.id:
                        rem = i
                        break
                particles = particles[0:rem]+particles[rem+1:]

print(len(particles))
