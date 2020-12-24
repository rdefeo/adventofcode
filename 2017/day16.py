#!/usr/bin/env python3

programs = list('abcdefghijklmnop')

dance = open('day16.txt','r').read().strip()

dance_steps = dance.split(',')

#programs = list('abcde')
#dance_steps = 's1,x3/4,pe/b'.split(',')

def routine():
    global programs
    for s in dance_steps:
        if s[0] == 's':
            #print("spin:",s)
            spin = int(s[1:])%len(programs)
            programs = programs[-spin:]+programs[:-spin]
        elif s[0] == 'x':
            #print("exch:",s)
            x1,x2 = map(int,s[1:].split('/'))
            p1,p2 = programs[x1],programs[x2]
            programs[x1] = p2
            programs[x2] = p1
        elif s[0] == 'p':
            #print("part:",s)
            p1,p2 = s[1:].split('/')
            for i,p in enumerate(programs):
                if p == p1:
                    programs[i] = p2
                    continue
                if p == p2:
                    programs[i] = p1
        else:
            print("Unknown dance step!",s)


routine()
print("Part 1:",''.join(programs))


# For Part 2, we need to run this 1B times. That will take forever.
# So let's see if the pattern cycles..
orig = list('abcdefghijklmnop')
programs = orig

seen = dict()
cycle_length = 0
for r in range(1000000000):
    p = ''.join(programs)
    if p not in seen:
        seen[p] = r
    else:
        print("Cycle! first:",seen[p]," most recent: ",r)
        cycle_length = r-seen[p]
        print("Cycle length:",cycle_length)
        break
    routine()

# Now that we know the cycle length, we can use modulo math
# to see how many cycles we need to actually run to reach 1B
remainder = 1000000000 % 60
for r in range(remainder):
    routine()
print("Part 2:",''.join(programs))


