import re
import sys
import os
import copy
import math
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

    index = 0

    tops = []

    for line in lines:
        L = line
        index = 11
        obj = {}
        while "," in line:
            res = re.search("\[\d+,\d+\]", line)
            a, b = res.group()[1:-1].split(",")
            a = int(a)
            b = int(b)
            if a > 10:
                a = obj[a]
            if b > 10:
                b = obj[b]

            obj[index] = (a, b)
            line = re.sub("\[\d+,\d+\]", str(index), line, 1)

            index += 1
        top = obj[int(line)]
        tops.append(top)

    def addleft(obj, num):
        if type(obj) is tuple:
            l, r = obj
            return (addleft(l, num), r)
        return obj + num

    def addright(obj, num):
        if type(obj) is tuple:
            l, r = obj
            return (l, addright(r, num))
        return obj + num

    def try_explode(obj, depth):
        if type(obj) is not tuple:
            return False, 0, 0, obj

        l, r = obj

        if depth >= 4:
            assert((type(l) is not tuple) and (type(r) is not tuple))
            return True, l, r, 0

        suc, lcar, rcar, res = try_explode(l, depth+1)
        if suc:
            return True, lcar, 0, (res, addleft(r, rcar))

        suc, lcar, rcar, res = try_explode(r, depth+1)
        if suc:
            return True, 0, rcar, (addright(l, lcar), res)

        return False, 0, 0, (l, r)


    def try_split(obj):
        if type(obj) is tuple:
            l, r = obj
            lsuc, lres = try_split(l)
            if lsuc:
                return True, (lres, r)
            rsuc, rres = try_split(r)
            if rsuc:
                return True, (lres, rres)
            return False, (l, r)

        if obj > 9:
            rd = int(math.floor(obj/2))
            ru = int(math.ceil(obj/2))
            return True, (rd, ru)

        return False, obj

    def simpl(t):
        while True:
            suc, lcar, rcar, res = try_explode(t, 0)
            if suc:
                t = res
                continue
            suc, res = try_split(t)
            if suc:
                t = res
                continue
            break
        return t


    def mag(o):
        if type(o) is tuple:
            l, r = o
            return 3*mag(l) + 2*mag(r)
        return o

    t = tops[0]
    for add in tops[1:]:
        t = (t, add)
        t = simpl(t)

    ans1 = mag(t)

    for i, a in enumerate(tops):
        for j, b in enumerate(tops):
            if i == j:
                continue
            ans2 = max(ans2, mag(simpl((a, b))))

    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


