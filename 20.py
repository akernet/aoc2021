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
        #nums = [[int(v) for v in line.strip()] for line in fc.split("\n")]
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]

    enh = pars[0][0]
    ans1, ans2 = 0, 0

    image = pars[1]
    activep = set()
    for row, line in enumerate(image):
        for col, c in enumerate(line):
            if c == "#":
                activep.add((row, col))


    def transform(inputset, invert):
        minr, maxr, minc, maxc = 0, 0, 0, 0
        for p in inputset:
            r, c = p
            minr = min(minr, r)
            maxr = max(maxr, r)
            minc = min(minc, c)
            maxc = max(maxc, c)
        outp = set()
        for r in range(minr-5, maxr+5):
            for c in range(minc-5, maxc+5):
                def get(rr, cc):
                    if (rr, cc) in inputset:
                        if invert:
                            return "0"
                        else:
                            return "1"
                    if invert:
                        return "1"
                    else:
                        return "0"
                row0 = [get(r-1, c-1), get(r-1, c), get(r-1, c+1)]
                row1 = [get(r, c-1), get(r, c), get(r, c+1)]
                row2 = [get(r+1, c-1), get(r+1, c), get(r+1, c+1)]
                binary = "".join(row0 + row1 + row2)
                index = int(binary, 2)

                if (enh[index] == "#") and invert:
                    outp.add((r, c))
                if (enh[index] != "#") and not invert:
                    outp.add((r, c))
        return outp

    ans1 = len(transform(transform(activep, False), True))
    invert = False
    out = activep
    for _ in range(50):
        out = transform(out, invert)
        invert = not invert
    ans2 = len(out)


    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


