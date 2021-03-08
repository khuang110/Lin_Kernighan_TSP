import math, random
from euclideanGraph import Graph


# Class for Lin Kernighan
class LKTsp(Graph):
    def __init__(self, _k):
        Graph.__init__(self, _k)
        self.dist = [[]]
        self.tour = []
        self.len_ = 0

    # Creates a random tour
    def init_tour(self):
        tmp = [i for i in range(0, self._k)]
        random.shuffle(tmp)
        self.tour = tmp
        self.len_ = len(tmp)

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
                if tour_idx[i] == x and tour_idx[i+1] == y:
                    return False
                if tour_idx[i] == y and tour_idx[i+1] == x:
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
                    curr_edge[j] = None
                    ln -= 1
                    break
        for edge in y:
            curr_edge.append(edge)
            ln += 1

        return tour_from_edges(curr_edge, ln)

    def get_y_edges(self, tour):
        """ This function just returns a list of vertices from tour
        :arg:
            tour (int): tour
        :return:
            Edge: returns list of edge objects to be added
        """
        res = []
        for i in range(0, self.len_):
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
        for i in range(0, self.len_):
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


def get_tour_prime(tour_idx, i):
    return tour_idx[0:i+2]


def tour_from_edges(curr_edge, ln):
    tour = [-1]*ln
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
        for k in range(0, len(curr_edge)):
            if curr_edge[j] is None:
                continue
            e = curr_edge[j]
            if e is not None and e.v1 == end:
                end = e.v2
                break
            elif e is not None and e.v2 == end:
                end = e.v1
                break
        if j == len(curr_edge):
            break

        curr_edge[j] = None

        tour[j] = end
        j += 1

    return tour


class Edge:
    # v1: vertex 1
    # v2: vertex 2
    def __init__(self, i, j):
        self.v1 = i if i > j else j
        self.v2 = j if i > j else i



