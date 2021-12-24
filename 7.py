import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

testpath = sys.argv[0].replace("py", "in")
samplepath = sys.argv[0].replace("py", "sample")

def solve(infile, p2):
    if not os.path.exists(infile):
        print("no file", infile)
        return

    with open(infile) as file:
        fc = file.read().strip()
        if len(fc) == 0:
            print("no content in file", infile)
            return

        lines = [line.strip() for line in fc.split("\n")]
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]

    pos = [int(x) for x in lines[0].split(",")]
    ans = 9999999999999999999999
    anspos = None

    memo = {}
    def cost(dis):
        if not p2:
            return dis
        if dis in memo:
            return memo[dis]
        cost = 1
        ans = 0
        while dis > 0:
            dis -= 1
            ans += cost
            cost += 1
        memo[dis] = ans
        return ans
    print(sum(pos))
    for center in range(-10, max(pos)):
        tryy = 0
        print(center)
        for p in pos:
            tryy = tryy + cost(abs(center-p))
        if tryy < ans:
            ans = tryy
            anspos = center
    print(ans, anspos)

print("sample")
solve(samplepath, False)

print("test")
solve(testpath, False)
solve(testpath, True)


