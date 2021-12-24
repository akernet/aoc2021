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

        lines = [int(x) for x in lines]

        pre = None
        ans1 = 0
        for line in lines:
            if pre is None:
                pre = line
                continue
            if line > pre:
                ans1 += 1
            pre = line

        pre  = None
        ans2 = 0
        for pos in range(0, len(lines)-2):
            values = lines[pos:pos+3]
            values_sum = sum(values)

            if pre is None:
                pre = values_sum
                continue

            if values_sum > pre:
                ans2 += 1
            pre = values_sum

        print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


