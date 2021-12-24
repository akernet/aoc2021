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

        def getcount(lines, banned):
            count0 = {}
            count1 = {}
            for line in lines:
                for pos, val in enumerate(line):
                    if pos in banned:
                        continue
                    if val == "0":
                        count0[pos] = count0.get(pos, 0) + 1
                    if val == "1":
                        count1[pos] = count1.get(pos, 0) + 1
            return (count0, count1)

        def getmax(d):
            maxkey = None
            for key in d:
                if maxkey is None or d[key] > d[maxkey]:
                    maxkey = key
            if maxkey is None:
                return None
            return (maxkey, d[maxkey])
        def getmin(d):
            minkey = None
            for key in d:
                if minkey is None or d[key] < d[minkey]:
                    minkey = key
            if minkey is None:
                return None
            return (minkey, d[minkey])
        def getgamma():
            banned = set()
            gamma = ""
            for pos in range(len(lines[0])):
                count0, count1 = getcount(lines, banned)
                most0 = count0[pos]
                most1 = count1[pos]
                if most0 > most1:
                    gamma = gamma + "0"
                else:
                    gamma = gamma + "1"
            return gamma
        def geteps():
            banned = set()
            gamma = ""
            for pos in range(len(lines[0])):
                count0, count1 = getcount(lines, banned)
                most0 = count0[pos]
                most1 = count1[pos]
                if most0 < most1:
                    gamma = gamma + "0"
                else:
                    gamma = gamma + "1"
            return gamma

        print(int(getgamma(), 2) * int(geteps(), 2))


        def getoxgen():
            cand = set(lines)
            pos = 0
            assert(len(lines) == len(cand))
            while len(cand) != 1:
                count0, count1 = getcount(list(cand), set())
                #print("ox", pos, cand, count1[pos], count0[pos])
                if count1[pos] >= count0[pos]:
                    for c in list(cand):
                        if c[pos] == "0":
                            cand.discard(c)
                else:
                    for c in list(cand):
                        if c[pos] == "1":
                            cand.discard(c)

                pos += 1
            return list(cand)[0]

        def getscrub():
            cand = set(lines)
            pos = 0
            assert(len(lines) == len(cand))
            while len(cand) != 1:
                count0, count1 = getcount(list(cand), set())
                #print("ox", pos, cand, count1[pos], count0[pos])
                if count1[pos] < count0[pos]:
                    for c in list(cand):
                        if c[pos] == "0":
                            cand.discard(c)
                else:
                    for c in list(cand):
                        if c[pos] == "1":
                            cand.discard(c)

                pos += 1
            return list(cand)[0]

        print(int(getoxgen(), 2) * int(getscrub(), 2))



print("sample")
solve(samplepath)

print("test")
solve(testpath)


