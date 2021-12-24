import re
import sys
import os
import copy
from collections import defaultdict as dd
# d = dd(lambda: 0)

import numpy as np
import math

cache = {}
def rotation_matrix(axis, theta):
    key = (axis, theta)
    if key in cache:
        return cache[key]

    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    cache[key] = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    return cache[key]

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

    scanner_points = []
    for p in pars:
        l = []
        for li in p[1:]:
            dx, dy, dz = li.split(",")
            dx = int(dx)
            dy = int(dy)
            dz = int(dz)

            l.append((dx, dy, dz))

        scanner_points.append(l)

    def rotations(vecs):
        axisl = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        degl = [0, math.pi/2, math.pi, 3*math.pi/2]
        ret = []

        for xrot in degl:
            for yrot in degl:
                for zrot in degl:
                    loc = []
                    for v in vecs:
                        v = np.dot(rotation_matrix(axisl[0], xrot), v)
                        v = np.dot(rotation_matrix(axisl[1], yrot), v)
                        v = np.dot(rotation_matrix(axisl[2], zrot), v)

                        loc.append(tuple([int(round(x)) for x in v]))

                    ret.append(loc)

        return ret


    def overlap(i, j):
        refpoints = set(scanner_points[i])

        matchingp = scanner_points[j]
        maxu = 0
        rotated = rotations(matchingp)
        offsets = None
        rotans = None
        for rotid, r in enumerate(rotated):
            rotatedset = set(r)

            for p1 in refpoints:
                for p2 in rotatedset:
                    ofx = p2[0]-p1[0]
                    ofy = p2[1]-p1[1]
                    ofz = p2[2]-p1[2]

                    shifted = []
                    for p3 in rotatedset:
                        x, y, z = p3
                        x -= ofx
                        y -= ofy
                        z -= ofz
                        shifted.append((x, y, z))

                    shiftedset = set(shifted)
                    u = refpoints.intersection(shiftedset)
                    if len(u) > maxu:
                        maxu = len(u)
                        offsets = ofx, ofy, ofz
                        rotans = rotid
        return maxu, offsets, rotans

    n = len(scanner_points)
    alpoints = set()
    ans = 0

    scanneroffs = {}
    scanneroffs[0] = (0, 0, 0)

    visited = set()
    def trav(i, off):
        if i in visited:
            return
        visited.add(i)
        print(len(visited))
        for j in range(n):
            if i == j:
                continue

            overl, offsets, rotans = overlap(i, j)
            if overl >= 12:
                points = scanner_points[j]
                rotated = rotations(points)[rotans]
                scanner_points[j] = rotated

                dx, dy, dz = off[0]+offsets[0], off[1]+offsets[1], off[2]+offsets[2]
                if j not in scanneroffs:
                    scanneroffs[j] = (-dx, -dy, -dz)
                for p in rotated:
                    x, y, z = p
                    x, y, z = x-dx, y-dy, z-dz
                    alpoints.add((x, y, z))
                trav(j, (dx, dy, dz))



    trav(0, (0, 0, 0))
    ans2 =0
    #print(scanneroffs)

    for p1 in scanneroffs:
        for p2 in scanneroffs:
            x1, y1, z1 = scanneroffs[p1]
            x2, y2, z2 = scanneroffs[p2]
            dis = abs(x1-x2) + abs(y1-y2) + abs(z1 - z2)
            #print(p1, p2, dis)

            ans2 = max(dis, ans2)


    print(len(alpoints), ans2)

print("sample")
solve(samplepath)

print("test")
solve(testpath)


