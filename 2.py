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

    # a
    hor = 0
    dep = 0

    for line in lines:
        com, num = line.split()
        num = int(num)

        if com == "down":
            hor += num
        elif com == "up":
            hor -= num
        elif com == "forward":
            dep += num

    print(hor*dep)

    # b
    hor = 0
    dep = 0
    aim = 0

    for line in lines:
        com, num = line.split()
        num = int(num)

        if com == "down":
            aim += num
        elif com == "up":
            aim -= num
        elif com == "forward":
            hor += num
            dep += aim*num

    print(hor*dep)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


