"""
TODO:
    - Create Algorithm Class with methods : input, output (path), run
    - Create 3 algorithms A-star, BFS, UCS that inherit from Algorithm Class
    - Use Environment Class to draw and check the valid moves.
"""
from __future__ import print_function
from environment import Environment
from object import Polygon
from object import distance

import numpy as np
import heapq


WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

class Algorithm():
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list):
        self.E = Environment(xmax, ymax, start_point, end_point, polygon_list)
        self.start_point = start_point
        self.end_point = end_point
        self.path = []
        self.fre = {}
        self.trace = {}

    def output(self):
        pass

    def run(self):
        pass
    def total_cost(self):
        pass
    def imitate_environment(self):
        self.path = self.output()
        self.E.draw_environment()
        if (len(self.path) != 0):
            self.E.draw_path(self.path)
        self.E.end_draw()

class UCS(Algorithm):
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list):
        super().__init__(xmax, ymax, start_point, end_point, polygon_list)
        self.d = {}
        for i in range(xmax + 1):
            for j in range(ymax + 1):
                self.d[(i, j)] = WMAX
                self.fre[(i, j)] = 1
                self.trace[(i, j)] = -1

        self.d[self.start_point] = 0

    def output(self):
        if (self.trace[self.end_point] == -1):
            print("There is no path from {} to {}".format(self.start_point, self.end_point))
            return []
        else:
            print('Path from {} to {}:'.format(self.start_point, self.end_point))
            trace_path = []
            while (self.start_point != self.end_point):
                trace_path.append(self.end_point)
                self.end_point = self.trace[self.end_point]

            trace_path.append(self.start_point)
            # trace_path = reversed(trace_path)
            for p in trace_path:
                print(p)
            # print(trace_path)
            return np.array(trace_path)

    def run(self):
        print("UCS Algorithm:\n")
        pq = []
        heapq.heappush(pq, (0, self.start_point))
        while len(pq) > 0:
            w, p = heapq.heappop(pq)

            print("Choose ", p)
            print("Cost at choose point: ", self.d[p])

            if (self.fre[p] == 0): continue
            if (p == self.end_point): break
            self.fre[p] = 0
            px, py = p
            for i in range(8):
                next_p = (px + dx[i], py + dy[i])
                w_move = 1
                if ((i == 0) | (i == 2) | (i == 4) | (i == 6)): #cross move
                    w_move = np.sqrt(2)
                if ((self.E.is_valid_point(next_p) == True) & (self.E.is_valid_move(p, next_p))):
                    if ((self.fre[next_p] == 1) & (self.d[next_p] > self.d[p] + w_move)):
                        self.d[next_p] = self.d[p] + w_move
                        heapq.heappush(pq, (self.d[next_p], next_p))
                        self.trace[next_p] = p
        self.cost = self.d[self.end_point]
        print("Total Cost: ", self.cost)
        self.imitate_environment()

class ASTAR(Algorithm):
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list):
        super().__init__(xmax, ymax, start_point, end_point, polygon_list)
        self.d = {}
        self.h = {}
        self.f = {}
        for i in range(xmax + 1):
            for j in range(ymax + 1):
                self.d[(i, j)] = WMAX
                self.h[(i, j)] = distance((i, j), end_point)
                self.f[(i, j)] = WMAX
                self.fre[(i, j)] = 1
                self.trace[(i, j)] = -1

        self.d[self.start_point] = 0
        self.f[self.start_point] = self.h[self.start_point]

    def output(self):
        if (self.trace[self.end_point] == -1):
            print("There is no path from {} to {}".format(self.start_point, self.end_point))
            return []
        else:
            print('Path from {} to {}:'.format(self.start_point, self.end_point))
            trace_path = []
            while (self.start_point != self.end_point):
                trace_path.append(self.end_point)
                self.end_point = self.trace[self.end_point]

            trace_path.append(self.start_point)
            # trace_path = reversed(trace_path)
            for p in trace_path:
                print(p)
            # print(trace_path)
            print("Total cost :", self.total_cost())
            return np.array(trace_path)

    def total_cost(self):
        return self.d[end_point]

    def run(self):

        pq = []
        heapq.heappush(pq, (self.f[self.start_point], self.start_point))
        while len(pq) > 0:
            w, p = heapq.heappop(pq)

            if (self.fre[p] == 0): continue
            if (p == self.end_point): break
            self.fre[p] = 0
            px, py = p
            for i in range(8):
                next_p = (px + dx[i], py + dy[i])
                w_move = 1
                if ((i == 0) | (i == 2) | (i == 4) | (i == 6)): #cross move
                    w_move = np.sqrt(2)
                if ((self.E.is_valid_point(next_p) == True) & (self.E.is_valid_move(p, next_p))):
                    if ((self.fre[next_p] == 1) & (self.f[next_p] > self.f[p] + w_move + self.h[next_p])):
                        self.d[next_p] = self.d[p] + w_move
                        self.f[next_p] = self.f[p] + w_move + self.h[next_p]
                        heapq.heappush(pq, (self.f[next_p], next_p))
                        self.trace[next_p] = p
        self.cost = self.d[self.end_point]
        self.imitate_environment()

class BFS(Algorithm):
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list):
        super().__init__(xmax, ymax, start_point, end_point, polygon_list)
        for i in range(xmax + 1):
            for j in range(ymax + 1):
                self.fre[(i, j)] = 1
                self.trace[(i, j)] = -1


if __name__ == '__main__':
    xmax, ymax = 22, 18
    start_point, end_point = (1, 1), (19, 16)
    polygon_point_list = np.array([[[4, 4], [5, 9], [8, 10], [9, 5]]
                                      , [[8, 12], [8, 17], [13, 12]]
                                      , [[11, 1], [11, 6], [14, 6], [14, 1]]
                                      , [[15, 11], [12, 9], [15, 6], [19, 10]]
                                    , [[2,3], [3,3],[4,0],[2,0]]])

    polygon_list_object = np.array([])

    for polygon_coord in polygon_point_list:
        print(polygon_coord)
        P = Polygon(polygon_coord)
        polygon_list_object = np.append(polygon_list_object, [P])


    AstarAlgo = ASTAR(xmax, ymax, start_point, end_point, polygon_list_object)
    AstarAlgo.run()

    UCSAlgo = UCS(xmax, ymax, start_point, end_point, polygon_list_object)
    UCSAlgo.run()