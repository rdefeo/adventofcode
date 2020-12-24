#!/usr/bin/env python3

steps = 386
insertions = 2017

#steps = 3

spinlock = [0]
pos = 0
value = 1
print(pos,spinlock)
for i in range(insertions+1):
    pos = (pos+steps) % len(spinlock)
#    print("inserting ",value,"at position", pos)
    spinlock = spinlock[:pos+1] + [value] + spinlock[pos+1:]
    pos += 1
    value += 1
#    print(pos,spinlock)
print(spinlock)
ind = spinlock.index(2017)
print(spinlock[ind-3:ind+3])

print("Part 2")
# So... it looked like ALL spinlocks started with value '0'
# It also means we don't really need to keep track of the list manipulations
# and instead just perform the math of moving (pos) forward, while
# incrementing (value) and our spinlock length - huh, I think they're
# the same! Now, we just need to remember the last value we inserted
# after position zero, in (iaz)
insertions = 50000000
spinlock = [0]
pos = 0
value = 1
len_spin = 1
iaz = 0

for i in range(insertions+1):
    pos = (pos+steps) % len_spin
    if pos == 0:
        iaz = value
    len_spin += 1
    pos += 1
    value += 1

print(iaz)
