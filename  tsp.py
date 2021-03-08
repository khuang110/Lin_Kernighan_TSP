#!/usr/bin/python
# https://www.researchgate.net/publication/227414913_Lin-Kernighan_Heuristic_Adaptations_for_the_Generalized_Traveling_Salesman_Problem
# https://ieeexplore.ieee.org/document/6771089
from lin_kernighan import *
import sys, re

# Usage: python3 tsp.py "input_file" "output_file"


def main():
    lns = process_lines(read_file("tsp_example_0.txt"))
    lkh = lns[0]
    lkh.find_sets()
    lkh.init_distance_table()
    lkh.init_tour()
    from pprint import pprint
    print("g")
    pprint(lkh.g)

    # print("sets")
    # pprint(lkh.sets)
    print("\ndist arry")
    print(lkh.dist)
    print("\ntour")
    print(lkh.tour)
    print("\nids")
    print(lkh.ids)
    lkh.run_lk()
    print("\ntour")
    print(lkh.tour)


# extract data from graph.txt
def read_file(in_file):
    lines = []

    with open(in_file, 'r') as r:
        lines = [line.rstrip() for line in r]
    return lines


# process data from the files
def process_lines(lines):

    test_cases = []
    curr = 0
    i = 0
    while i < len(lines):
        # k: number of vertices
        k = int(lines[i])

        g = LKTsp(k)
        # loop through ordered pairs and put in graph
        for k in range(i + 1, k + i + 1):
            v = lines[k].split()
            # Add vertex x,y points to graph
            # Add city id's to dict where coordinates are key
            s = {int(v[0]): (int(v[1]), int(v[2]))}
            g.ids.update(s)
            g.add_vertex(int(v[1]), int(v[2]))
        # Shift i to move to next graph
        i = k + 1
        curr += 1
        test_cases.append(g)
    return test_cases


if __name__=="__main__":
    main()
