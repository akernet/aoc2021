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

    inn = [int(x) for x in lines[0].split(",")]

    def popafter(inn, days):
        pop = inn
        for i in range(days):
            newpop = []
            for ind in pop:
                if ind-1 == -1:
                    newpop.append(8)
                    newpop.append(6)
                else:
                    newpop.append(ind-1)
            pop = newpop

        return pop
    print(len(popafter(inn, 80)))

    memo = {}
    def poplenafter(inn, days):
        arg = (inn, days)
        if arg in memo:
            return memo[arg]
        pop = [inn]
        for i in range(days):
            newpop = []
            for ind in pop:
                if ind-1 == -1:
                    newpop.append(8)
                    newpop.append(6)
                else:
                    newpop.append(ind-1)
            pop = newpop

        memo[arg] = len(pop)
        return memo[arg]

    ans2 = 0
    popafter100 = popafter(inn, 100)

    for p in popafter100:
        ans2 += poplenafter(p, 156)

    print(ans2)


print("sample")
#solve(samplepath)

print("test")
solve(testpath)


