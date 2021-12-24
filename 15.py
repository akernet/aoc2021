import re
import sys
import os
import copy
import heapq
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
        nums = [[int(v) for v in line.strip()] for line in fc.split("\n")]
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]

    def solve(mapp):
        R = len(mapp)
        C = len(mapp[0])

        queue = []
        heapq.heappush(queue, (0, (0, 0)))
        visited = set()
        while queue:
            prio, top = heapq.heappop(queue)

            if top in visited:
                continue
            visited.add(top)

            r, c = top
            if r < 0 or r >= R:
                continue
            if c < 0 or c >= C:
                continue
            curval = mapp[r][c]
            if (r, c) == (R-1, C-1):
                ans = prio + curval
                break

            newval = prio + curval
            if top == (0, 0) and prio == 0:
                newval = 0

            heapq.heappush(queue, (newval, (r, c+1)))
            heapq.heappush(queue, (newval, (r, c-1)))
            heapq.heappush(queue, (newval, (r+1, c)))
            heapq.heappush(queue, (newval, (r-1, c)))
        return ans

    ans1 = solve(nums)

    R = len(lines)
    C = len(lines[0])

    cop = [[0 for _ in range(C*5)] for _ in range(R*5)]
    for rc in range(5):
        for cc in range(5):
            for r in range(R):
                for c in range(C):
                    cop[R*rc+r][C*cc+c] = nums[r][c] + rc + cc
                    while cop[R*rc+r][C*cc+c] > 9:
                        cop[R*rc+r][C*cc+c] -= 9

    ans2 = solve(cop)
    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


