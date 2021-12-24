import re
import sys
import os
import copy
from functools import lru_cache
from collections import defaultdict as dd

p1 = 8-1
p2 = 2-1

break_score = 21

@lru_cache(None)
def dp(p1pos, p2pos, p1score, p2score, p1turn):
    if p1score >= break_score:
        return (1, 0)
    if p2score >= break_score:
        return (0, 1)

    p1sum, p2sum = 0, 0
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                diesum = d1 + d2 + d3
                if p1turn:
                    newp1pos = (p1pos + diesum) % 10
                    s = newp1pos + 1
                    a, b = dp(newp1pos, p2pos, p1score+s, p2score, False)
                else:
                    newp2pos = (p2pos + diesum) % 10
                    s = newp2pos + 1
                    a, b = dp(p1pos, newp2pos, p1score, p2score+s, True)
                p1sum += a
                p2sum += b
    return p1sum, p2sum

a, b = dp(p1, p2, 0, 0, True)
if a > b:
    print(a)
else:
    print(b)
