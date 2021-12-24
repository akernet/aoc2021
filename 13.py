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

    dots = set()

    for line in pars[0]:
        row,col = line.split(",")
        row = int(row)
        col = int(col)
        dots.add((row, col))

    folds = []
    for f in pars[1]:
        s, po = f.split("=")
        po = int(po)
        if "x" in s:
            folds.append(("x", po))
        else:
            folds.append(("y", po))

    def do_f(dots, fold):
        newd = set()
        if fold[0] == "x":
            for d in dots:
                if d[0] > fold[1]:
                    newd.add((fold[1]-abs(fold[1]-d[0]), d[1]))
                else:
                    newd.add(d)
        else:
            for d in dots:
                if d[1] > fold[1]:
                    newd.add((d[0], fold[1]-abs(fold[1]-d[1])))
                else:
                    newd.add(d)

        return newd
    dots = do_f(dots, folds[0])
    print(len(dots))
    for f in folds[1:]:
        dots = do_f(dots, f)


    ys = [x[1] for x in dots]
    xs = [x[0] for x in dots]


    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            char = "."
            if (x, y) in dots:
                char = "#"
            print(char, end="")
        print()


print("sample")
solve(samplepath)

print("test")
solve(testpath)


