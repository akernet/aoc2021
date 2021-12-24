import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

testpath = sys.argv[0].replace("py", "in")
samplepath = sys.argv[0].replace("py", "sample")

def solve(infile, p2):
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
    ans0 = 0
    ans2 = 0

    connections = {}

    for line in lines:
        src, dst = line.strip().split("-")
        if src not in connections:
            connections[src] = []
        if dst not in connections:
            connections[dst] = []

        connections[src].append(dst)
        connections[dst].append(src)

    def traf(pos, visited, spoiled):
        if pos == "end":
            return 1
        if len(visited) > 0 and pos == "start":
            return 0

        if pos == pos.lower() and pos in visited and visited[pos] > 1:
            return 0
        if pos == pos.lower() and pos in visited and visited[pos] == 1 and spoiled:
            return 0
        if pos == pos.lower() and pos in visited and visited[pos] == 1:
            if not p2:
                return 0
            spoiled = True

        rv = 0
        visited[pos] = visited.get(pos, 0) + 1
        for con in connections[pos]:
            rv += traf(con, visited, spoiled)
        visited[pos] = visited[pos] - 1
        return rv

    ans0 = traf("start", {}, False)


    print(ans0)

print("sample")
#solve(samplepath, False)

print("test")
solve(testpath, False)
solve(testpath, True)


