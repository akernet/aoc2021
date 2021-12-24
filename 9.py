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

    ans1 = 0
    ans2 = 0
    data = [[int(x) for x in list(y)] for y in lines]

    basinspoints = []
    def get(row, col):
        if row < 0 or row >= len(data):
            return 999999999999
        if col < 0 or col >= len(data[0]):
            return 999999999999
        return data[row][col]

    for row in range(len(data)):
        for col in range(len(data[0])):
            if get(row, col) < min([get(row+1, col), get(row-1, col), get(row, col+1), get(row, col-1)]):
                ans1 += get(row, col) + 1
                basinspoints.append((row, col))

    taken = set()
    sizes = {}
    for idd, basin in enumerate(basinspoints[1:]):
        if basin in taken:
            continue

        sizes[idd] = 0

        def exp(row, col):
            if get(row, col) >= 9:
                return
            if (row, col) in taken:
                return

            sizes[idd] += 1
            taken.add((row, col))
            exp(row+1, col)
            exp(row-1, col)
            exp(row, col+1)
            exp(row, col-1)

        exp(basin[0], basin[1])

    largest = sorted(sizes.values(), reverse=True)[0:3]
    ans2 = largest[0]*largest[1]*largest[2]

    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


