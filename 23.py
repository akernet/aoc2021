import re
import sys
import os
import copy

import heapq
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

        lines = [line for line in fc.split("\n")]
        #nums = [[int(v) for v in line.strip()] for line in fc.split("\n")]
        pars = [[row.strip() for row in par.split("\n")] for par in fc.split("\n\n")]

    if p2:
        lines = lines[0:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + lines[3:]

    R = len(lines)
    C = len(lines[0])
    ans1 = 0
    ans2 = 0

    walls = set()
    hallway = set()
    A, B, C, D = set(), set(), set(), set()

    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            coord = (r, c)
            if col == "#":
                walls.add(coord)
            if col == "A":
                A.add(coord)
            if col == "B":
                B.add(coord)
            if col == "C":
                C.add(coord)
            if col == "D":
                D.add(coord)
            if col == ".":
                hallway.add(coord)

    destroomcol = set()
    destrooms = A|B|C|D
    for (r, c) in destrooms:
        destroomcol.add(c)

    def valid(state):
        A, B, C, D = state
        A = set(A)
        B = set(B)
        C = set(C)
        D = set(D)
        al = A|B|C|D

        if len(al) != len(A) + len(B) + len(C) + len(D):
            return False

        if len(al&walls) > 0:
            print(al, walls)
            return False


        return True

    def finished(state):
        A, B, C, D = state

        A = set(A)
        B = set(B)
        C = set(C)
        D = set(D)

        al = A|B|C|D
        if len(al & destrooms) != len(al):
            return False

        for (r, c) in A:
            if c != destroomcol_list[0]:
                return False

        for (r, c) in B:
            if c != destroomcol_list[1]:
                return False

        for (r, c) in C:
            if c != destroomcol_list[2]:
                return False

        for (r, c) in D:
            if c != destroomcol_list[3]:
                return False

        return True

    queue = []

    destroomcol_list = list(destroomcol)
    destroomcol_list.sort()

    startA = [x for x in A]
    startB = [x for x in B]
    startC = [x for x in C]
    startD = [x for x in D]
    heapq.heappush(queue, (0, (startA, startB, startC, startD)))

    def get_path(start, dest, obs):
        queue2 = []
        heapq.heappush(queue2, (0, start))
        obs.discard(start)
        visited = set()

        ans = None
        while queue2:
            prio, pos = heapq.heappop(queue2)

            if pos in obs:
                continue

            if pos == dest:
                ans = prio
                break

            if pos in visited:
                continue
            visited.add(pos)

            r, c = pos
            heapq.heappush(queue2, (prio+1,(r+1, c)))
            heapq.heappush(queue2, (prio+1, (r-1, c)))
            heapq.heappush(queue2, (prio+1,(r, c+1)))
            heapq.heappush(queue2, (prio+1,(r, c-1)))

        return ans

    vis = set()

    def visualize(top):
        rows = len(lines)
        cols = len(lines[0])
        A, B, C, D = [set(x) for x in top]
        for r in range(rows):
            for c in range(cols):
                char = " "
                pos = (r, c)
                if (r,c) in walls:
                    char = "#"
                if pos in destrooms:
                    char = "-"
                if pos in A:
                    char = "A"
                if pos in B:
                    char = "B"
                if pos in C:
                    char = "C"
                if pos in D:
                    char = "D"

                sys.stdout.write(char)
            print()

    lasttop = None
    iterr = 0
    maxsize = 0
    while queue:
        iterr += 1
        maxsize = max(maxsize, len(queue))

        prio, top = heapq.heappop(queue)
        lasttop = top
        if prio % 1000 == 0:
            print(prio, len(queue))
            visualize(top)

        visobj = tuple([tuple(sorted(x)) for x in top])
        if visobj in vis:
            continue
        vis.add(visobj)

        if not valid(top):
            continue

        if finished(top):
            ans1 = prio
            break

        A, B, C, D = top

        tomove = [A, B, C, D]
        rooms = [set(), set(), set(), set()]

        ocu = set()
        for typindex, G in enumerate(tomove):
            for coord in G:
                ocu.add(coord)
                r, c = coord
                if coord in destrooms:
                    roomindex = destroomcol_list.index(c)
                    rooms[roomindex].add(typindex)

        for typindex, G in enumerate(tomove):
            cost = [1, 10, 100, 1000][typindex]

            for character in G:
                if character in hallway:
                    # find way to room at typindex
                    # is it valid to enter?
                    fault = False
                    for c in rooms[typindex]:
                        # if not break
                        if c != typindex:
                            fault = True

                    if fault:
                        continue

                    for d in destrooms:
                        dr, dc = d
                        if d in ocu:
                            continue
                        if dc != destroomcol_list[typindex]:
                            continue

                        lowerdown = (dr+1, dc)
                        if lowerdown in destrooms and lowerdown not in ocu:
                            continue

                        lengthtodest = get_path(character, d, ocu|walls)
                        if lengthtodest is not None:
                            newstate = ([], [], [], [])
                            for typindex2, G2 in enumerate(tomove):
                                for char2 in G2:
                                    if char2 != character:
                                        newstate[typindex2].append(char2)
                            newstate[typindex].append(d)
                            heapq.heappush(queue, (prio + lengthtodest*cost, newstate))

                else:
                    for dest in hallway:
                        hr, hc = dest
                        # if the hallway is not above a wall
                        if (hr+1, hc) not in walls:
                            continue

                        if dest in ocu:
                            continue

                        lengthtodest = get_path(character, dest, ocu|walls)
                        if lengthtodest is not None:
                            newstate = ([], [], [], [])
                            for typindex2, G2 in enumerate(tomove):
                                for char2 in G2:
                                    if char2 != character:
                                        newstate[typindex2].append(char2)
                            newstate[typindex].append(dest)
                            heapq.heappush(queue, (prio + lengthtodest*cost, newstate))


    visualize(top)
    print(ans1, maxsize)

print("sample")
#solve(samplepath, False)

print("test")
solve(testpath, False)
solve(testpath, True)


