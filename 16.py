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
    ans1, ans2 = 0, 0

    bits = []
    nibs = lines[0]
    for nib in nibs:
        dec = int(nib, 16)
        bi = bin(dec)[2:].rjust(4, "0")
        for b in range(4):
            bits.append(bi[b])

    def take(pointer, bi, numb):
        if pointer >= len(bi):
            return (-1, 0)
        bi = bi[pointer:pointer+numb]
        if len(bi) == 0:
            return (-1, 0)
        pointer += numb
        return (pointer, todec(bi))


    def todec(ar):
        return int("".join(ar), 2)

    def solve(bits, count, depth):
        offset = 0
        version_sum = 0

        vals = []

        num_packets = 0
        while num_packets < count and offset+3+3+1 < len(bits):
            num_packets += 1
            packet_start = offset

            offset, version = take(offset, bits, 3)
            offset, typeid = take(offset, bits, 3)

            print("  "*depth, typeid, version)

            version_sum += version

            if typeid == 4:
                total = ""
                while True:
                    offset, five = take(offset, bits, 5)
                    last = five < 0b10000
                    five = five & 0b01111
                    binary = bin(five)[2:].rjust(4, "0")
                    total += binary
                    if last:
                        break
                vals.append(int(total, 2))
            else:
                offset, variant = take(offset, bits, 1)
                if variant == 0:
                    offset, length = take(offset, bits, 15)
                    internalvals, _, internalsum = solve(bits[offset:offset+length], 1e9, depth+1)
                    version_sum += internalsum
                    offset += length
                else:
                    offset, internal_count = take(offset, bits, 11)
                    internalvals, internaloffset, internalsum = solve(bits[offset:], internal_count, depth+1)
                    offset += internaloffset
                    version_sum += internalsum
                if typeid == 0:
                    vals.append(sum(internalvals))
                elif typeid == 1:
                    tot = 1
                    for v in internalvals:
                        tot *= v
                    vals.append(tot)
                elif typeid == 2:
                    vals.append(min(internalvals))
                elif typeid == 3:
                    vals.append(max(internalvals))
                elif typeid == 5:
                    assert len(internalvals) == 2

                    if internalvals[0] > internalvals[1]:
                        vals.append(1)
                    else:
                        vals.append(0)
                elif typeid == 6:
                    assert len(internalvals) == 2

                    if internalvals[0] < internalvals[1]:
                        vals.append(1)
                    else:
                        vals.append(0)
                elif typeid == 7:
                    assert len(internalvals) == 2

                    if internalvals[0] == internalvals[1]:
                        vals.append(1)
                    else:
                        vals.append(0)


        return vals, offset, version_sum




    ans2, _, ans1 = solve(bits, 1e9, 0)

    print(ans1, ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


