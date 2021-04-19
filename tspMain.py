#!/usr/bin/env python3
from tspSolver import *
import sys, os
from time import perf_counter


def main(argv):
    """ Driver function
    :param:
        argv (list): In file name
    """
    path, f_loc = get_path(argv[0])
    if f_loc is None:
        raise FileNotFoundError("File not found!")

    # Create Distance table
    lns = process_lines(read_file(f_loc))
    lkh = lns[0]
    lkh.find_sets()
    lkh.init_distance_table()
    hg = to_solver(lkh)

    # Time algorithm
    t1_start = perf_counter()
    # Run algorithm
    tour, weight = hg.run()
    t1_end = perf_counter()
    print("Running time:", (t1_end-t1_start))

    to_file(argv[0]+".tour", tour, weight, path)


def get_path(file_name):
    """ This function searches for a given file name in current and subdirectories
        and returns the path.
    :param:
        file_name (string): Name of file to search for
    :return:
        string, string: file path, file path with file appended
    """
    root_dir = os.path.dirname(__file__)

    for sub_dir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == file_name:
                return sub_dir, os.path.join(sub_dir, file)
    return None, None


# extract data from graph.txt
def read_file(in_file):
    """ This function parses a file and returns list of lines from file
    :param:
        in_file (string): name of file to be parsed
    :return:
        list: return a list of lines
    """
    lines = []

    with open(in_file, 'r') as r:
        lines = [line.rstrip() for line in r]
    return lines


# process data from the files
def process_lines(lines):
    """ This function processes lines from a file and creates list of distance obj
    :param:
        lines (list): List of lines
    :return:
        list: list of distance obj
    """

    test_cases = []
    curr = 0
    i = 0
    while i < len(lines):
        # k: number of vertices
        k = int(lines[i])

        g = Distance(k)
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


def to_file(outfile, tour, weight, path):
    """ This function outputs to a file
    :param:
        outfile (string): name of output file
    :param:
        tour (list): Solution to tsp
    :param:
        weight (int): Total weight of path
    :param:
        path (string): Path to file location
    :return:
        file: file output
    """
    out = os.path.join(path, outfile)
    with open(out, 'w') as w:
        w.write(str(weight)+"\n")
        for i in range(len(tour)-1):
            w.write(str(tour[i])+"\n")
        w.close()


if __name__=="__main__":
    sys.setrecursionlimit(10400)
    main(sys.argv[1:])
