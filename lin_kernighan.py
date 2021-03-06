import itertools # Used to find all possible sets
import math


# Disjoint set
# Union - Find
class Set:
    # set: disjoint set of vertices
    # ln: length of set
    def __init__(self, n):
        self.set = [-1]*n
        self.ln = 0

    # Create a union of two sets
    def union(self, v1, v2):
        if self.set[v1] < self.set[v2]:
            self.set[v1] = v2
        else:
            if self.set[v1] == self.set[v1]:
                self.set[v1] -= 1
            self.set[v2] = v1
        self.ln += 1

    # Find value in set
    def find(self, r):
        x = r[0] + r[1]
        if self.set[x] < 0:
            return x
        n = 0
        while self.set[n] > 0:
            n = self.set[n]
        return n


# Definition of graph
class Graph:
    # _k: number of vertices
    # g: graph, adjacency matrix implementation
    # sets: list of disjoint sets
    def __init__(self, _k):
        self._k = _k
        self.sets = {}
        self.g = []
        self.ids = {}

    # Add a vertex to graph
    def add_vertex(self, x, y):
        self.g.append([x, y])

    # help sort, return calculation to sort by
    def help_sort(self, s):
        d = calc_distance(s[0])
        return d

    # Go through graph and find all possible sets
    def find_sets(self):
        idx = 0
        s = {}
        # Itertool.combinations finds all possible sets
        for i in itertools.combinations(self.g, 2):
            c = calc_distance(i)
            # add sets to a dict.
            p = {idx: [i, c]}
            s.update(p)
            idx += 1
        self.sets = [val for key, val in s.items() if val != -1]
        # Move sets to sorted list
        # No need to have it put in a dict first, too lazy to remove it..
        self.sets.sort(key=self.help_sort)

    # Creates a random tour
    def init_tour(self):
        


# Calculate euclidean distance
def calc_distance(set_):
    x1, y1 = set_[0]
    x2, y2 = set_[1]
    distance = math.sqrt((x1-x2)**2+(y1-y2)**2)
    return round(distance)


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

        g = Graph(k)
        # loop through ordered pairs and put in graph
        for k in range(i + 1, k + i + 1):
            v = lines[k].split()
            # Add vertex x,y points to graph
            # Add city id's to dict where coordinates are key
            g.ids = {(int(v[1]), int(v[2])): int(v[0])}
            g.add_vertex(int(v[1]), int(v[2]))
        # Shift i to move to next graph
        i = k + 1
        curr += 1
        test_cases.append(g)
    return test_cases
