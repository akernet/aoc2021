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

    downmoving = set()
    rightmoving = set()

    for r, line in enumerate(lines):
        for c, col in enumerate(line):
            if col == ">":
                rightmoving.add((r, c))
            elif col == "v":
                downmoving.add((r, c))

    rows = len(lines)
    cols = len(lines[0])

    def getnextright(c):
        if c == cols-1:
            return 0
        return c+1
    def getnextdown(r):
        if r == rows-1:
            return 0
        return r+1


    step = 0
    while True:
        moved = False

        blocked = downmoving | rightmoving
        newright = set()
        newdown = set()

        sortedright = sorted(rightmoving, key=lambda x: x[1], reverse=True)

        for coord in sortedright:
            r, c = coord
            newcoord = (r, getnextright(c))
            if newcoord in blocked:
                # dont move
                newright.add(coord)
            else:
                moved = True
                r, c = coord
                newright.add(newcoord)

        blocked = downmoving | newright
        sorteddown = sorted(downmoving, key=lambda x: x[0], reverse=True)

        for coord in sorteddown:
            r, c = coord
            newcoord = (getnextdown(r), c)
            if newcoord in blocked:
                # dont move
                newdown.add(coord)
            else:
                moved = True
                r, c = coord
                newdown.add(newcoord)

        step += 1

        rightmoving = newright
        downmoving = newdown

        for r in range(rows):
            for c in range(cols):
                char = "."
                if (r, c) in newright:
                    char = ">"
                if (r, c) in newdown:
                    char = "v"
                print(char, end="")
            print()
        print("\n"*3)

        #if step > 10:
        #    break

        if not moved:
            break

    ans1 = step



    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


