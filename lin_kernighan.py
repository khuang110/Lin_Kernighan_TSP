#!/usr/bin/env python3
import math, random, sys
from euclideanGraph import Graph


# Class for Lin Kernighan
class LKTsp(Graph):
    def __init__(self, _k=0):
        Graph.__init__(self, _k)
        self.dist = [[]]
        self.tour = []
        self.len_ = 0
        self.path = []

    # Creates a random tour
    def init_tour(self):
        tmp = [i for i in range(0, self._k)]
        random.shuffle(tmp)
        self.tour = tmp
        self.len_ = len(tmp)

    def get_length(self):
        return self._k

    # Get previous town id
    def get_prev_id(self, i):
        return self.len_-1 if i == 0 else i-1

    # Get next town id
    def get_next_id(self, i):
        return (i+1) % self.len_

    # Create a table with all the distances
    def init_distance_table(self):
        print(self._k)
        self.dist = [[0]*self._k for i in range(self._k)]
        for i in range(0, self._k):
            for j in range(0, self._k):
                # Calculate inner product of all combinations of sets
                self.dist[i][j] = int(round(math.sqrt((self.g[i][0]-self.g[j][0])**2+(self.g[i][1]-self.g[j][1])**2)))

    def get_tour_dist(self):
        distance = 0
        for k in range(0, self.len_):
            i = self.tour[k]
            j = self.tour[(k+1) % self.len_]
            distance += self.dist[i][j]
        return distance

    def get_dist(self, id1, id2):
        # distance between two tours
        return self.dist[self.tour[id1]][self.tour[id2]]

    def get_index(self, id_):
        """ This function returns the index of the node based off the id of the node
            in the tour
        :arg:
            id_ (int): The id of the town

        :return:
            int: index of town in tour
        """
        i = 0
        for town in self.tour:
            if id_ is town:
                return i
            else:
                i += 1
        return -1

    def get_neighbor(self, curr):
        """ This function returns the nearest neighbor to a given town
        :arg:
            curr (int): Current town index

        :return:
             int: Nearest town index
        """
        curr_vertex = self.tour[curr]
        nearest_town = -1
        min_dist = 2147483647
        for i in range(self._k):
            if i != curr_vertex:
                dist = self.get_dist(i, curr_vertex)
                if dist < min_dist:
                    nearest_town = self.get_index(i)
                    min_dist = dist
        return nearest_town

    def check_valid_tour(self, tour2):
        if len(tour2) != self.len_:
            return False
        else:
            for i in range(0, self.len_-1):
                for j in range(0, self.len_):
                    if tour2[i] == tour2[j]:
                        return False
        return True

    def select_tour(self, tour_idx):
        """ This function selects a new tour
        :arg:
            tour_idx ([int]): tour index array

        :return:
            int: tour that is selected
        """
        n1 = self.get_prev_id(tour_idx[len(tour_idx)-1])
        n2 = self.get_next_id(tour_idx[len(tour_idx)-1])
        tour = self.create_tour(self.tour, tour_idx, n1)

        if self.check_valid_tour(tour):
            return n1
        else:
            tour2 = self.create_tour(self.tour, tour_idx, n2)
            if self.check_valid_tour(tour2):
                return n2
        return -1

    def improve(self, curr, prev=False):
        """ This function improves the tour.
        :arg:
            prev (bool): Bool if this is the previous town
                (default is false)
        :arg:
            curr (int): Current town index

        :return:
            void
        """
        id2 = self.get_prev_id(curr) if prev else self.get_next_id(curr)
        id3 = self.get_neighbor(id2)

        if id3 != -1 and self.get_dist(id2, id3) < self.get_dist(curr, id2):
            self.lk(curr, id2, id3)
        elif not prev:
            # Condition for previous id
            self.improve(curr, True)

    def run_lk(self):
        old_gain = 0
        new_gain = self.get_tour_dist()

        while True:
            old_gain = new_gain
            for i in range(0, self.len_):
                self.improve(i)
            new_gain = self.get_tour_dist()
            # Base case if no more improvements can be made
            if new_gain >= old_gain:
                break

    def lk(self, id1, id2, id3):
        """ This function is the driver of the lin-kernighan algorithm
        :arg:
            id1 (int): id of first town
        :arg:
            id2 (int): id of second town
        :arg:
            id3 (int): id of third town
        :return:
            void
        """
        tour_idx = [-1, id1, id2, id3]
        gain = self.get_dist(id2, id3) - self.get_dist(id3, id2)
        i = 3
        gt = 0
        for j in range(4, self.len_**10, 2):
            new_id = self.select_tour(tour_idx)
            # This case should not evaluate according to LK paper
            if new_id == -1:
                break
            ii = self.next_y(tour_idx)
            if ii == -1:
                break

            gain += self.get_dist(tour_idx[len(tour_idx)-2], new_id)
            dff = gain - self.get_dist(new_id, id1)
            print("dff: ", dff)
            if dff > gt:
                i = j
                gt = dff
            gt -= self.get_dist(new_id, ii)
            tour_idx.append(ii)

        if gt > 0:
            tour_idx[i+1] = tour_idx[1]
            self.tour = get_tour_prime(tour_idx, i)

    def next_x(self, tour_idx, i):
        return self.check_connection(tour_idx, i, self.get_next_id(i)) or\
               self.check_connection(tour_idx, i, self.get_prev_id(i))

    def check_connection(self, tour_idx, x, y):
        if x == y:
            return False
        else:
            for i in range(1, len(tour_idx)-1, 2):
                x, y = self.ids[tour_idx[i]]
                if x == x and y == y:
                    return False
                if x == y and y == x:
                    return False
        return True

    def check_positive_gain(self, tour_idx, j):
        gain = 0
        for i in range(0, len(tour_idx) - 2):
            id1 = tour_idx[i]
            id2 = tour_idx[i + 1]
            id3 = j if i == len(tour_idx) - 3 else tour_idx[i + 2]
            gain += self.get_dist(id2, id3) - self.get_dist(id1, id2)
        return gain > 0

    def next_y(self, tour_idx):
        j = tour_idx[len(tour_idx)-1]
        new_y = []
        for i in range(0, len(tour_idx)):
            if not self.check_positive_gain(tour_idx, j):
                continue
            if not self.check_disjoint(tour_idx, i, j):
                continue
            if not self.next_x(tour_idx, i):
                continue
            new_y.append(i)

        min_dist = 2147483647
        min_id = -1
        for i in range(0, len(new_y)):
            d = self.get_dist(j, i)
            if d < min_dist:
                min_dist = d
                min_id = i
        return min_id

    def get_edges_from_tour(self, tour):
        """ This function just returns a list of vertices from tour
        :arg:
            tour (int): tour
        :return:
            Edge: returns list of edge objects
        """
        res = []
        for i in range(0, len(tour)):
            if tour[i] == -1:
                x, y = -1, -1
            else:
                x, y = self.ids[tour[i]]
            e = Edge(x, x)
            res.append(e)
        return res

    def create_tour(self, tour, tour_idx, val=-1):
        """ This function adds a value to tour
        :arg:
            tour_idx ([int]): tour index array
        :arg:
            val (int): value to be added to tour
                (Default -1)
        :return:
            adds val to tour
        """
        t = tour_idx
        if val != -1:
            t.append(val)
            t.append(t[1])
        curr_edge = self.get_edges_from_tour(tour)
        x = self.get_x_edges(t)
        y = self.get_y_edges(t)
        ln = len(curr_edge)

        for edge in x:
            for j in range(0, len(curr_edge)):
                e = curr_edge[j]
                if e == edge:
                    curr_edge.remove(curr_edge[j])
                    ln -= 1
                    break
        for edge in y:
            print(edge.v1, edge.v2)
            curr_edge.append(edge)
            ln += 1

        return self.tour_from_edges(curr_edge, ln)

    def create_eulerian_tour(self, tour, tour_idx):
        queue = [[[], tour[0], tour]]

        while queue:
            path, node, unvisited = queue.pop()
            path += [node]

            if not unvisited:
                return path
            for edge in unvisited:
                if node in edge:
                    queue += [[path, next_node(node, edge)]]

    def hierholzer(self, tour_idx):
        start = tour_idx[0]
        tour = [start]
        traversed = {}
        idx = 0

        while len(traversed) // 2 < len(self.sets) and idx < len(tour):
            subset = []

    def dfs(self, u, root, subset, traversed):
        for v in self.dist[u]:
            if (u, v) not in traversed or (v, u) not in traversed:
                traversed[(u, v)] = traversed[(v, u)] = True
                subset.append(v)
                if v == root:
                    return
                else:
                    self.dfs(u, root, subset, traversed)

    def get_y_edges(self, tour):
        """ This function just returns a list of vertices from tour
        :arg:
            tour (int): tour
        :return:
            Edge: returns list of edge objects to be added
        """
        res = []
        for i in range(2, self.len_-1):
            if tour[i] == -1:
                x, y = -1, -1
            else:
                x, y = self.ids[tour[i]]
            e = Edge(x, y)
            res.append(e)
        return res

    def get_x_edges(self, tour):
        """ This function just returns a list of vertices from tour
        :arg:
            tour (int): tour
        :return:
            Edge: returns list of edge objects to be added
        """
        res = []
        for i in range(1, self.len_-2):
            if tour[i] == -1:
                x, y = -1, -1
            else:
                x, y = self.ids[tour[i]]
            e = Edge(x, y)
            res.append(e)
        return res

    def check_disjoint(self, tour_idx, i, j):
        """ This funciton checks if an edge is ready in the set
        :param:
            tour_idx ([int]): list of tour index
        :param:
            i (int): index of an endpoint
        :param:
            j (int): index of an endpoint
        :return:

        """
        if i == j:
            return False
        for k in range(0, len(tour_idx)):
            x, y = self.ids[k]
            if x == i and y == j:
                return False
            if x == j and y == i:
                return False
        return True

    def tour_from_edges(self, curr_edge, ln):
        tour = [-1 for i in range(ln)]
        end = -1
        i = 0
        for i in range(0, len(curr_edge)):
            if curr_edge[i] is not None:
                tour[0] = curr_edge[i].v1
                tour[1] = curr_edge[i].v2
                end = tour[1]
                break
        curr_edge[i] = None
        j = 2
        while True:
            k = 0
            if j >= ln:
                break
            for k in range(0, len(self.ids)):
                if curr_edge[j] is None:
                    continue
                e = curr_edge[j]
                x, y = self.ids[k]
                if e is not None and e.v1 == x:
                    end = k
                    break
                elif e is not None and e.v2 == y:
                    end = k
                    break
            if j == len(curr_edge):
                break

            curr_edge[j] = None

            tour[j] = end
            j += 1

        return tour



def get_tour_prime(tour_idx, i):
    return tour_idx[0:i+2]


def next_node(curr, edge):
    return edge[0] if curr == edge[1] else edge[1]


def remove_edge(queue, to_rm):
    return [i for i in queue if i != to_rm]


def to_hungarian(obj):
    return Hungarian(obj.get_length(), obj.dist)


def transpose(m):
    res = [[] for i in range(len(m[0]))]

    for i in range(len(m)):
        for j in range(len(m[0])):
            res[j].append(m[i][j])
    return res


def upper_left(a, n):
    # Matrix a
    return [[a[i][j] for j in range(n)] for i in range(n)]


def lower_right(a, n):
    # Matrix a
    return [[a[i][j] for j in range(len(a)-n, len(a))] for i in range(len(a)-n, len(a))]


class Edge:
    # v1: vertex 1
    # v2: vertex 2
    def __init__(self, i, j):
        self.v1 = i if i > j else j
        self.v2 = j if i > j else i

    def __eq__(self, other):
        if self.v1 == other.v1 and self.v2 == other.v2:
            return True
        else:
            return False


class Hungarian:
    def __init__(self, k, dist):
        self._k = k
        self.dist = dist
        self.zeros = [[0]*self._k for i in range(self._k)]
        self.lines = [[0]*self._k for i in range(self._k)]

        for i in range(k):
            for j in range(k):
                if i == j:
                    self.dist[i][j] = sys.maxsize

    def max(self, i, j):
        col = 0
        row = 0

        for k in range(self._k):
            if self.dist[i][k] == 0:
                row += 1

        for k in range(self._k):
            if self.dist[k][j] == 0:
                col += 1

        return col if col > row else row * -1

    def minimize_row(self):
        # Step 1
        res = []
        m = -1
        for row in self.dist:
            m = min(row, key=(lambda x: x if x > 0 and x > m else 2**10))
            res.append(list(map((lambda x: x - m if x > m else 0), row)))
        self.dist = res

    def minimize_col(self):
        # Step 2
        res = []
        for row in transpose(self.dist):
            m = min(row)
            if m < 0:
                res.append(row)
                continue
            else:
                res.append(list(map((lambda x: x - m if x > m else 0), row)))
        # for i in range(self._k):
        #     col = []
        #     for j in range(self._k):
        #         col.append(self.dist[j][i])
        #     m = min(col, key=(lambda x: x if x > 0 and x > m else 2**10))
        #     if m <= 0:
        #         res.append(col)
        #         continue
        #     else:
        #         res.append(list(map((lambda x: x - m if x > m else 0), col)))

        self.dist = transpose(res)

    def check_zeros_col(self):
        sum_zeros = 0
        for row in range(len(self.dist)):
            for col in self.dist[row]:
                if col == 0:
                    sum_zeros += 1
        return sum_zeros == self._k

    def clear_neighbor(self, i, j):
        if self.zeros[i][j] > 0:
            for k in range(self._k):
                if self.zeros[k][j] > 0:
                    # Clear neighbor
                    self.zeros[k][j] = 0
                # Add line
                self.lines[k][j] = 1
        else:
            for k in range(self._k):
                if self.zeros[i][k] < 0:
                    # Clear neighbor
                    self.zeros[i][k] = 0
                # Add line
                self.lines[i][k] = 1
        self.lines[i][j] = 1
        self.zeros[i][j] = 0

    def get_min_uncovered(self):
        # Get the min of all the uncovered elements
        res = []
        for i in range(self._k):
            for j in range(self._k):
                if self.lines[i][j] == 0:
                    if self.dist[i][j] < 0:
                        res.append(0)
                    else:
                        res.append(self.dist[i][j])
        if not res:
            return -1
        else:
            return min(res)

    def add_min_to_covered(self, min_):
        # Add min uncovered to covered

        for i in range(self._k):
            for j in range(self._k):
                if self.lines[i][j] == 0:      # Covered lines
                    self.dist[i][j] -= min_ if self.dist[i][j] >= min_ else 0
                elif self.lines[i][j] == 1:     # Uncovered lines
                    self.dist[i][j] += min_

    def sub_min(self, min_):
        # subtract min from whole matrix
        for i in range(self._k):
            for j in range(self._k):
                self.dist[i][j] -= min_ #if self.dist[i][j] >= min_ else 0

    def cover_zeros(self):
        # Step 3
        for i in range(self._k):
            for j in range(self._k):
                if abs(self.zeros[i][j]) > 0:
                    self.clear_neighbor(i, j)

    def get_num_lines(self):
        count = 0
        for row in self.lines:
            if all(j == 1 for j in row):
                count += 1
        for col in transpose(self.lines):
            if all(j == 1 for j in col):
                count += 1

        return count

    def max_matching(self):
        visited = [[]]*2
        visited[0] = [-1 for _ in range(self._k)]

        res_row = 0
        for i in range(self._k):
            visited[1] = [False for _ in range(self._k)]
            if self.bipartite_match(i, visited):
                res_row += 1

    def bipartite_match(self, i, visited):
        # Depth first search
        for j in range(self._k):
            if self.zeros[i][j] != 0 and visited[1][j] is False:
                visited[1][j] = True
                if visited[0][j] == -1 or self.bipartite_match(visited[0][j], visited):
                    visited[0][j] = i
                    return True
        return False

    def run(self):
        #for i in range(self._k):
        self.minimize_row()                              # Step 1
        if self.check_zeros_col():                       # Step 2
            self.minimize_col()
            # else:
            #     break

        while True:

            [print(row) for row in self.dist]
            # self.zeros = [[0] * self._k for i in range(self._k)]
            # self.lines = [[0] * self._k for i in range(self._k)]
            for i in range(self._k):
                for j in range(self._k):
                    if self.dist[i][j] == 0:
                        self.zeros[i][j] = self.max(i, j)

            self.cover_zeros()                           # Step 3
            if self.get_num_lines() == self._k:           # Step 4
                break

            print("LIENS")
            [print(row) for row in self.lines]

            min_ = self.get_min_uncovered()
            #if min_ == 0:

            self.add_min_to_covered(min_)
            self.sub_min(min_)
           # [print(row) for row in self.lines]
            print()
        [print(row) for row in self.lines]

    def find_path(self, weight, path, idx, lst):
        if len(path) == self._k:
            # Add path back to home
            path.append(path[0])
            weight.append(lst[0][idx])
            print("end of weight")
            print(lst[0][idx])
            return
        lst2 = []
        for i, ele in enumerate(lst[idx]):
            if i not in path:
                lst2.append(ele)
            else:
                self.dist[idx][i] = sys.maxsize
                lst2.append(sys.maxsize)
        m = min(lst2)

        idx = lst[idx].index(m)
        if idx not in path:
            path.append(idx)
            weight.append(m)
            # Call function and swap row/ col
            self.find_path(weight, path, idx, lst)

    def find_path_itr(self, weight, path, idx, lst):
        # Iterative find path
        while len(path) < self._k:
            lst2 = []
            for i, ele in enumerate(lst[idx]):
                if i not in path:
                    lst2.append(ele)
                else:
                    self.dist[idx][i] = sys.maxsize
                    lst2.append(sys.maxsize)
            m = min(lst2)

            idx = lst[idx].index(m)
            if idx not in path:
                path.append(idx)
                weight.append(m)

            if len(path) == self._k:
                # Add path back to home
                path.append(path[0])
                weight.append(lst[0][idx])
                print("end of weight")
                print(lst[0][idx])
                return

    def run3(self):
        m = max(self.dist[0])
        idx = self.dist[0].index(m)
        weight = []
        tour = [idx]

        dist_e2 = (transpose(self.dist[::-1]))[::-1]
        self.find_path_itr(weight, tour, idx, dist_e2)
        # for i in range(2, self._k):
        #     loc_weight = []
        #     loc_tour = [idx]
        #     sub_dist = upper_left(self.dist, i)
        #     self.find_path(loc_weight, tour, idx, sub_dist)
        #     weight.append(sum(loc_weight))
        #     print("loc weight")
        #     print(sum(loc_weight))
        print("run3 weight")
        print(sum(weight))

    def run2(self):
        sys.setrecursionlimit(10400)

        m = max(self.dist[0])
        idx = self.dist[0].index(m)
        # Home index
        print("IDX")
        print(idx)
        weight = []
        tour = [idx]

        self.find_path(weight, tour, idx, self.dist)
        print("PATH")
        print(tour)
        print("WEIGHT")
        print(weight)
        print(self._k)
        print("LEN WEIGHT")
        print(len(weight))
        print("sum weight")
        print(sum(weight))

        return tour



