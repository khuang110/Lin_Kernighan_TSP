#!/usr/bin/env python3
import math, sys
from euclideanGraph import Graph
import copy


class Distance(Graph):
    def __init__(self, _k=0):
        Graph.__init__(self, _k)
        self.dist = [[]]
        self.len_ = 0
        self.path = []

    def get_length(self):
        return self._k

    # Create a table with all the distances
    def init_distance_table(self):
        """ Function to initialize distance table with max int on diagonal

        :return:
            distance table
        """
        self.dist = [[0]*self._k for i in range(self._k)]
        for i in range(0, self._k):
            for j in range(0, self._k):
                # Calculate inner product of all combinations of sets
                self.dist[i][j] = int(round(math.sqrt((self.g[i][0]-self.g[j][0])**2+(self.g[i][1]-self.g[j][1])**2)))


def to_solver(obj):
    """ Function to create solver object
    :param:
        obj (Distance obj): Distance obj to convert
    :return:
        obj: solver object
    """
    return Solver(obj.get_length(), obj.dist)


class Solver:
    """
    Solver class. Runs the algorithm to find 2 opt path
    """
    def __init__(self, k, dist):
        self._k = k
        self.dist = dist
        self.zeros = [[0]*self._k for i in range(self._k)]
        self.lines = [[0]*self._k for i in range(self._k)]

        for i in range(k):
            for j in range(k):
                if i == j:
                    self.dist[i][j] = sys.maxsize

    def find_path(self, weight, path, idx, lst):
        """ Function to find the shortest path. Greedy algorithm.
        :param:
            weight (list): List of weights
        :param:
            path (list): list of vertices visited
        :param:
            idx (int): Current index
        :param:
            lst (list): List of distances
        :return:
            path, weight: path and weight will be optimal found
        """
        if len(path) == self._k:
            # Add path back to home
            path.append(path[0])
            weight.append(lst[path[0]][idx])
            return

        lst2 = []
        for i, ele in enumerate(lst[idx]):
            if i not in path:
                lst2.append(ele)
            else:
                lst[idx][i] = sys.maxsize
                lst2.append(sys.maxsize)
        m = min(lst2)
        idx = lst[idx].index(m)

        if idx not in path:
            path.append(idx)
            weight.append(m)
            # Call function and swap row/ col
            self.find_path(weight, path, idx, lst)

    def find_path_itr(self, weight, path, idx, lst):
        """ Function to find the shortest path. Greedy algorithm.
        :param:
            weight (list): List of weights
        :param:
            path (list): list of vertices visited
        :param:
            idx (int): Current index
        :param:
            lst (list): List of distances
        :return:
            path, weight: path and weight will be optimal found
        """
        # Iterative find path
        while len(path) < self._k:
            lst2 = []
            for i, ele in enumerate(lst[idx]):
                if i not in path:
                    lst2.append(ele)
                else:
                    lst[idx][i] = sys.maxsize
                    lst2.append(sys.maxsize)
            m = min(lst2)

            idx = lst[idx].index(m)
            if idx not in path:
                path.append(idx)
                weight.append(m)

            if len(path) == self._k:
                # Add path back to home
                path.append(path[0])
                weight.append(lst[path[0]][idx])
                return

    def run(self):
        """ This function runs the algorithm.
        :return:
            list, int: list of vertices visited in order, Weight of path found.
        """
        tour = [[] for i in range(self._k)]
        weight = [[] for i in range(self._k)]
        weight2 = []
        min_weight = sys.maxsize

        n = self._k if self._k < 300 else 420%69
        for i in range(n):
            d = copy.deepcopy(self.dist)
            m = max(self.dist[i])
            idx = self.dist[i].index(m)
            tour[i].append(idx)
            self.find_path(weight[i], tour[i], idx, d)

        min_tour = []
        for i in range(n):
            sum_l = sum(weight[i])
            if sum_l < min_weight:
                min_weight = sum_l
                min_tour = tour[i]
        print(min_weight)
        return min_tour, min_weight


