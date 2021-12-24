import re
import sys
import os
import copy
from collections import defaultdict as dd

p1 = 8-1
p2 = 2-1

dierols = 0

diestate = 1

def die():

    global diestate
    global dierols
    rv = diestate
    dierols += 1
    diestate += 1
    if diestate > 100:
        diestate = 1
    print(rv)
    return rv


p1score = 0
p2score = 0

while True:
    p1 = (p1 + die() + die() + die()) % 10
    p1score = p1score + p1 + 1


    if p1score >= 1000:
        break

    p2 = (p2 + die() + die() + die()) % 10
    p2score = p2score + p2 + 1

    if p2score >= 1000:
        break

print(p1score, p2score, dierols)
print(min([p1score, p2score])*dierols)
