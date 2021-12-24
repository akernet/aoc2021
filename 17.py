import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

testpath = sys.argv[0].replace("py", "in")
samplepath = sys.argv[0].replace("py", "sample")

def solve(infile):
    if not os.path.exists(infile):
        print("no file", infile)
        return

    with open(infile) as file:
        fc = file.read().strip()
        if len(fc) == 0:
            print("no content in file", infile)
            return

        lines = [line.strip() for line in fc.split("\n")]
        #nums = [[int(v) for v in line.strip()] for line in fc.split("\n")]
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]

    R = len(lines)
    C = len(lines[0])
    ans1 = 0
    ans2 = 0

    xtar = range(211,232+1)
    xtarmin = 211
    xtarmax = 232

    ytarmin = -124
    ytarmax = -69
    ytar = range(-124, -69+1)

    yout = -124

    def tryy(xvel, yvel):
        x, y = 0, 0
        maxy = 0
        good = False

        while True:
            x += xvel
            y += yvel
            maxy = max(y, maxy)

            if xvel > 0:
                xvel -= 1
            elif xvel < 0:
                xvel += 1
            yvel -= 1


            if (xtarmin <= x <= xtarmax) and (ytarmin <= y <= ytarmax):
                return maxy
            if y+1 < yout:
                return None
            if xvel == 0 and not (xtarmin <= x <= xtarmax):
                return None


    for xvel in range(1, 300):
        for yvel in range(-200, 1000):
            val = tryy(xvel, yvel)

            if val is None:
                continue
            ans2 += 1
            print(ans2)
            if val > ans1:
                ans1 = val

    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


