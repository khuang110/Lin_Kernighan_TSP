#!/usr/bin/python
#https://www.researchgate.net/publication/227414913_Lin-Kernighan_Heuristic_Adaptations_for_the_Generalized_Traveling_Salesman_Problem
from lin_kernighan import *
import sys, re

# Usage: python3 tsp.py "input_file" "output_file"


def main():
    print(process_lines(read_file("tsp_example_0.txt")))
    #print(read_input_vals("tsp_example_0.txt"))

# Borrowed from TSPAllVisited.py
def read_input_vals(in_file):
    # each line of in_file should have a label as its first int on each line,
    # this captures a list of those labels
    # (expected from 0 to n - 1, but only uniqueness is necessary)

    file = open(in_file, 'r')
    # toss the first line which is the number of points
    line = file.readline()
    line = file.readline()
    # points tracks the points as teh key and the number of visitations as the value at that key
    points = []
    x = []
    y = []
    while len(line) > 1:
        line_parse = re.findall(r'[^,;\s]+', line)
        points.append(line)
        x.append(line)
        y.append(line)
        line = file.readline()
    file.close()


    return points, x, y


if __name__=="__main__":
    main()
