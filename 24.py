import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

testpath = sys.argv[0].replace("py", "in")
samplepath = sys.argv[0].replace("py", "sample")

def solve(infile):
    global ans1
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

    instructions = []

    for line in lines:
        if "inp" in line:
            inp, target = line.split()
            instructions.append((inp, (target)))
        else:
            print(line)
            inst, target, source = line.split()
            instructions.append((inst, (target, source)))

    #print(instructions)

    ans1 = 0

    minprog = [1]*14

    visited = set()
    def dp(inst_id, w, x, y, z, input_values):
        global ans1
        key = (inst_id, w, x, y, z)
        if key in visited:
            #print(visited)
            return
        visited.add(key)

        #print(inst_id, w, x, y, z)

        if inst_id == len(instructions):
            #print(input_values)
            if z == 0:
                inputv = "".join([str(x) for x in input_values])
                ans1 = max(ans1, int(inputv))
                print(ans1)
                exit()
            return

        neww = w
        newx = x
        newy = y
        newz = z

        inst, vals = instructions[inst_id]

        def get(s):
            if s == "x":
                return x
            if s == "y":
                return y
            if s == "z":
                return z
            if s == "w":
                return w
            return int(s)



        if inst == "inp":
            for i in (range(1, 10)):
            #for i in reversed(range(1, 10)):
                #if len(input_values) == 0 and i >= 2:
                #    continue

                minprog[len(input_values)] = max(minprog[len(input_values)], i)
                print(minprog)

                target = vals
                input_values.append(i)
                if target == "x":
                    newx = i
                if target == "y":
                    newy = i
                if target == "z":
                    newz = i
                if target == "w":
                    neww = i


                dp(inst_id+1, neww, newx, newy, newz, input_values)
                input_values.pop()
        else:
            target, source = vals
            val = None
            if inst == "add":
                val = get(source) + get(target)
            elif inst == "mul":
                val = get(source)*get(target)
            elif inst == "div":
                val = get(target) // get(source)
            elif inst == "mod":
                val = get(target) % get(source)
            elif inst == "eql":
                if get(source) == get(target):
                    val = 1
                else:
                    val = 0
            else:
                print(inst)
                assert(False)

            if target == "x":
                newx = val
            if target == "y":
                newy = val
            if target == "z":
                newz = val
            if target == "w":
                neww = val

            dp(inst_id+1, neww, newx, newy, newz, input_values)


    dp(0, 0, 0, 0, 0, [])

    #print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


