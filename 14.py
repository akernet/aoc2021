import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

testpath = sys.argv[0].replace("py", "in")
samplepath = sys.argv[0].replace("py", "sample")

def solve(infile, steps):
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

    temp = pars[0][0]
    rules = pars[1]

    rul = {}
    for ru in rules:
        pair, tar = ru.split(" -> ")
        rul[pair] = tar

    counts = {}
    for r in range(len(temp)-1):
        sub = temp[r:r+2]
        counts[sub] = counts.get(sub, 0)+1

    for r in range(steps):
        new_c = {}
        for c in counts:
            #print(c)
            val = counts[c]
            sub = rul[c]
            first = c[0] + sub
            sec = sub + c[1]
            #print(first, sec, val)
            new_c[first] = new_c.get(first, 0) + val
            new_c[sec] = new_c.get(sec, 0) + val
        counts = new_c

    total = {}
    for c in counts:
        val = counts[c]
        total[c[0]] = total.get(c[0], 0) + val
    total[temp[len(temp)-1]] += 1

    print(max(total.values())-min(total.values()))
    #print(total)


print("sample")
solve(samplepath, 10)

print("test")
solve(testpath, 10)
solve(testpath, 40)


