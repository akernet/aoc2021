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

    R = len(lines)
    C = len(lines[0])
    ans1 = 0
    ans2 = 0

    on = set()

    boxes = []

    for line in lines:
        seton = False
        if "on" in line:
            seton = True

        onof, rest = line.split(" ")
        x, y, z = rest.split(",")
        x = x[2:].strip()
        y = y[2:].strip()
        z = z[2:].strip()
        print(x, y, z)
        xxx = [int(k) for k in x.split("..")]
        yyy = [int(k) for k in y.split("..")]
        zzz = [int(k) for k in z.split("..")]
        boxes.append((seton, tuple(xxx), tuple(yyy), tuple(zzz)))

        x1, x2 = xxx
        y1, y2 = yyy
        z1, z2 = zzz

        for xx in range(max(-50, x1), min(50, x2)+1):
            for yy in range(max(-50, y1), min(50, y2)+1):
                for zz in range(max(-50, z1), min(50, z2)+1):
                    if seton:
                        on.add((xx, yy, zz))
                    else:
                        on.discard((xx, yy, zz))
    ans1 = len(on)

    xsplits = set()
    ysplits = set()
    zsplits = set()

    for box in boxes:
        seton, xxx, yyy, zzz = box
        xmin, xmax = xxx
        xsplits.add(xmin)
        xsplits.add(xmax+1)

        ymin, ymax = yyy
        ysplits.add(ymin)
        ysplits.add(ymax+1)

        zmin, zmax = zzz
        zsplits.add(zmin)
        zsplits.add(zmax+1)




    def getsuperpixels(box):
        onoff, xxx, yyy, zzz = box

        totalpairs = []

        for index in range(3):
            axis = [xxx, yyy, zzz][index]
            refset = [xsplits, ysplits, zsplits][index]

            cmin, cmax = axis
            points = []
            pset = set()
            for ccc in range(cmin, cmax+1):
                if ccc in refset:
                    points.append(ccc)
                    pset.add(ccc)

            points = [cmin] + points
            points = points + [cmax]
            #print("po", points)

            pairs = []

            for i in range(len(points)-1):
                cor = 1
                if i == len(points)-2:
                    cor = 0
                pairs.append((points[i], points[i+1]-cor))


            totalpairs.append(pairs)

        superpixels = set()

        for xxx in totalpairs[0]:
            for yyy in totalpairs[1]:
                for zzz in totalpairs[2]:
                    superpixels.add((xxx, yyy, zzz))


        return superpixels

    if False:
        xsplits = set()
        xsplits.add(6)
        xsplits.add(10)
        ysplits = set()
        zsplits = set()
        ysplits.add(1)

        print(getsuperpixels((False, (2, 15), (0, 1), (0, 0))))
        exit()


    superpix = set()
    totalsum = 0

    ans2 = 0
    for index, box in enumerate(boxes):
        print(index, len(superpix))
        seton, xxx, yyy, zzz = box

        superp = getsuperpixels(box)
        for pix in superp:
            totalsum += 1
            if seton:
                superpix.add(pix)
            else:
                superpix.discard(pix)

    ans2 = 0
    print(len(superpix), totalsum)

    for sp in superpix:
        xxx, yyy, zzz = sp
        xmin, xmax = xxx
        ymin, ymax = yyy
        zmin, zmax = zzz
        ans2 += (xmax-xmin+1)*(ymax-ymin+1)*(zmax-zmin+1)

    print(ans1, ans2)
    #exit()

print("sample")
solve(samplepath)
print("test")
solve(testpath)



#ref 2758514936282235
#inc 2758481072261743
#inc 2758481072261743
#    2758481072261743
#    2759450491380727
#    2758948842578244
#2758514936282235