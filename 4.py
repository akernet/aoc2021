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

    calls = [x.strip() for x in pars[0][0].split(",")]

    def f(p):
        b = []
        for r in p:
            b.append(r.split())
        for i, call in enumerate(calls):
            m = 0
            for r in range(len(b)):
                for c in range(len(b[r])):
                    if b[r][c] == call:
                        assert(b[r][c] == b[r][c].strip())
                        m += 1
                        b[r][c] = "x"
            assert(m == 1 or m== 0)

            def ar(b):
                for r in range(5):
                    v = True
                    for c in range(5):
                        if b[r][c] != "x":
                            v = False
                    if v:
                        return True

                return False

            def ac(b):
                for c in range(5):
                    v = True
                    for r in range(5):
                        if b[r][c] != "x":
                            v = False
                    if v:
                        return True

                return False

            if ar(b) or ac(b):
                co = 0
                for r in range(5):
                    for c in range(5):
                        if b[r][c] != "x":
                            co += int(b[r][c])
                return (i, co*int(call))


    for p1 in [True, False]:
        minn = None
        cans = None
        for p in pars[1:]:
            pp = f(p)
            rw, ans = pp
            if minn is None or (p1 and rw <= minn) or (not p1 and rw >= minn):
                minn = rw
                cans = ans
        print(cans)



print("sample")
#solve(samplepath)

print("test")
solve(testpath)


