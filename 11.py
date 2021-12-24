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

    print(lines)
    print(pars)

    levels = []
    for line in lines:
        levels.append([int(x) for x in line])

    print(levels)

    C = len(levels[0])
    R = len(levels)
    ans1 = 0

    steps = 101
    if p2:
        steps = 1000000

    for step in range(1, steps):
        for r in range(len(levels)):
            for c in range(C):
                levels[r][c] += 1
        flashed = set()
        while True:
            some = False

            for r in range(R):
                for c in range(C):
                    if levels[r][c] > 9 and (r, c) not in flashed:
                        some = True
                        flashed.add((r, c))

                        def s(rr, cc):
                            if 0 <= rr < R and 0 <= cc < C:
                                #print("increasing", rr, cc)
                                levels[rr][cc] += 1

                        for rr in range(r-1, r+2):
                            for cc in range(c-1, c+2):
                                if rr == r and cc == c:
                                    continue
                                s(rr, cc)
            if not some:
                break
        for r, c in flashed:
            levels[r][c] = 0
        if len(flashed) == R*C:
            print("all", step)
            break
        ans1 += len(flashed)
    for r in levels:
        print(r)
    print(ans1)


print("sample")
#solve(samplepath, True)

print("test")
solve(testpath, False)
solve(testpath, True)


