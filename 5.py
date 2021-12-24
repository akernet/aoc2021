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
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]



    covered = {}

    for line in lines:
        p1, p2 = line.split(" -> ")
        row1, col1 = p1.split(",")
        row2, col2 = p2.split(",")
        row1 = int(row1)
        row2 = int(row2)
        col1 = int(col1)
        col2 = int(col2)
        def add(row, col):
            if (row, col) not in covered:
                covered[(row, col)] = 0
            covered[(row, col)] += 1

        if col1 != col2:

            if row1 != row2:
                continue
            minc = min(col1, col2)
            maxc = max(col1, col2)
            for cc in range(minc, maxc+1):
                add(row1, cc)
        if row1 != row2:
            if col1 != col2:
                continue
            minr = min(row1, row2)
            maxr = max(row1, row2)
            for rr in range(minr, maxr+1):
                add(rr, col1)

    ans = 0
    for key in covered:
        if covered[key] > 1:
            ans += 1

    print(ans)
print("sample")
solve(samplepath)

print("test")
solve(testpath)


