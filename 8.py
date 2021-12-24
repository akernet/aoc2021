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

    print(lines)
    print(pars)

    ans = 0
    ans2 = 0
    for line in lines:
        inn, out = line.split("|")
        inp = [x.strip() for x in inn.split()]
        outp = [x.strip() for x in out.split()]
        good = False
        for p in outp:
            if len(p) == len("fdgacbe") or len(p) == len("gcbe") or len(p) == len("cgb") or len(p) == len("gc"):
                ans += 1
                good = True

        onep = None
        fourp = None
        sevenp = None
        eightp = None

        twop = None
        threep = None
        fivep = None
        sixp = None
        ninep = None
        zerop = None

        for p in inp + outp:
            if len(p) == 2:
                onep = set(p)
            if len(p) == 4:
                fourp = set(p)
            if len(p) == 3:
                sevenp = set(p)
            if len(p) == 7:
                eightp = set(p)

        for p in inp + outp:
            if len(p) == 2:
                continue
            if len(p) == 4:
                continue
            if len(p) == 3:
                continue
            if len(p) == 7:
                continue

            sp = set(p)
            # 2
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 1
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 2
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 2
            if len(p) == 5 and couldmatchone and couldmatchfour and couldmatchsevenp:
                twop = sp
                continue

            # 3
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 2
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 3
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 3
            if len(p) == 5 and couldmatchone and couldmatchfour and couldmatchsevenp:
                threep = sp
                continue
            # 5
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 1
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 3
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 2
            if len(p) == 5 and couldmatchone and couldmatchfour and couldmatchsevenp:
                fivep = sp
                continue
            # 6
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 1
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 3
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 2
            if len(p) == 6 and couldmatchone and couldmatchfour and couldmatchsevenp:
                sixp = sp
                continue
            # 9
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 2
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 4
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 3
            if len(p) == 6 and couldmatchone and couldmatchfour and couldmatchsevenp:
                ninep = sp
                continue
            # 0
            couldmatchone = (not onep) or len(sp.intersection(onep)) == 2
            couldmatchfour = (not fourp) or len(sp.intersection(fourp)) == 3
            couldmatchsevenp = (not sevenp) or len(sp.intersection(sevenp)) == 3
            if len(p) == 6 and couldmatchone and couldmatchfour and couldmatchsevenp:
                zerop = sp
                continue
            # inconclusive
            print(sp)
            assert(False)

        num = ""
        for p in outp:
            sp = set(p)
            if sp == onep:
                num += "1"
            elif sp == zerop:
                num += "0"
            elif sp == twop:
                num += "2"
            elif sp == threep:
                num += "3"
            elif sp == fourp:
                num += "4"
            elif sp == fivep:
                num += "5"
            elif sp == sixp:
                num += "6"
            elif sp == sevenp:
                num += "7"
            elif sp == eightp:
                num += "8"
            elif sp == ninep:
                num += "9"
            else:
                print(sp)
                assert(False)

        ans2 += int(num)

    print(ans, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


