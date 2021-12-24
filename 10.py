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

    ans1 = 0
    ans2 = 0

    op = ["(","[","{", "<"]
    close = [")","]","}", ">"]
    score = {
        ")": 3,
        "]": 57,
        "}" :1197,
        ">" :25137
    }
    inc = []

    def check(line):
        stack = []

        for i in line:
            if i in op:
                stack.append(i)
            elif i in close:
                pos = close.index(i)
                if ((len(stack) > 0) and
                    (op[pos] == stack[len(stack)-1])):
                    stack.pop()
                else:
                    return score[i]
        inc.append(stack)
        return 0

    for line in lines:
        ans1+= check(line)

    scores = []
    for rem in inc:
        score = 0
        score2 = {
            "(": 1,
            "[": 2,
            "{" :3,
            "<" :4
        }
        while rem:
            top = rem.pop()
            score *= 5
            score += score2[top]
        scores.append(score)

    ans2 = sorted(scores)[len(scores)//2]

    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


