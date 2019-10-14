from environment import Environment
import numpy as np
from astar import ASTAR
from object import Polygon
import matplotlib.pyplot as plt

WMax = 1e9

def getbit(stt, i):
    return ((stt >> i) & 1)

def offbit(stt, i):
    return ((~(1 << i)) & stt)

class Route():
    def __init__(self, E):
        self.E = E
        self.start_point = E.start_point
        self.end_point = E.end_point
        self.path = []
        self.fre = {}
        self.trace = {}
        self.timeProcessing = 0
        self.cost = 0
        self.place = E.place

        self.all_point_list = [self.start_point]
        for point in self.place:
            self.all_point_list.append(point)
        self.all_point_list.append(self.end_point)

        n = len(self.all_point_list)
        self.matrix_cost = np.full((n, n), WMax)
        for i in range(n):
            self.matrix_cost[i][i] = 0.0
        self.matrix_path = np.full((n, n), None)
        for i in range(n):
            for j in range(i + 1, n):
                if i != j:
                    astarAlgo = ASTAR(self.all_point_list[i], self.all_point_list[j], self.E)
                    astarAlgo.run(0)
                    self.matrix_cost[i][j] = astarAlgo.cost
                    self.matrix_cost[j][i] = self.matrix_cost[i][j]
                    self.matrix_path[i][j] = astarAlgo.output()
                    self.matrix_path[j][i] = self.matrix_path[i][j]

    def draw_start_end(self):
        plt.scatter(self.start_point[0], self.start_point[1])
        plt.scatter(self.start_point[0], self.start_point[1] + 0.5, marker="$S$")

        plt.scatter(self.end_point[0], self.end_point[1])
        plt.scatter(self.end_point[0], self.end_point[1] + 0.5, marker="$G$")

    def find_path_list(self):
        DP = {}
        trace = {}
        n = len(self.all_point_list)
        for stt in range(2**n):
            for i in range(n):
                if (getbit(stt, i) == 1):
                    DP[(stt, i)] = WMax
                    prev = offbit(stt, i)
                    if (prev == 0):
                        if (i == 0):
                            DP[(stt, i)] = 0
                            trace[(stt, i)] = (0, 0)
                        else:
                            DP[(stt, i)] = WMax
                    else:
                        for j in range(n):
                            if (getbit(prev, j) == 1):
                                # DP[(stt, i)] = min(DP[(stt, i)], DP[(prev, j)] + self.matrix_cost[i][j])
                                # trace[(stt, i)] = (prev, j)
                                if (DP[(prev, j)] + self.matrix_cost[i][j] < DP[(stt, i)]):
                                    DP[(stt, i)] = DP[(prev, j)] + self.matrix_cost[i][j]
                                    trace[(stt, i)] = (prev, j)

        last = (2 ** n) - 1
        index = n - 1
        print("DP Cost : ", DP[(last, index)])
        path_list = []
        cost = 0
        while (last != 0):
            prev, j = trace[(last, index)]
            if (j != index):
                print("({} {} : {}):".format(j, index, self.matrix_cost[j][index]))
                path_list.append(self.matrix_path[j][index])
                if (len(self.matrix_path[j][index]) == 0):
                    return (None, None)
            cost += self.matrix_cost[index][j]
            last = prev
            index = j

        return (path_list, cost)



    def run(self):
        self.E.draw_environment()
        self.draw_start_end()
        self.E.draw_place()
        # path_list = [self.matrix_path[0][1], self.matrix_path[1][2],
        #              self.matrix_path[2][3], self.matrix_path[3][4], self.matrix_path[4][5]]
        # cost = self.matrix_cost[0][1] + self.matrix_cost[1][2] + self.matrix_cost[2][3] + self.matrix_cost[3][4] + self.matrix_cost[4][5]
        path_list, cost = self.find_path_list()
        if (path_list, cost) == (None, None):
            print("There is no path through required points!")
        else:

            print(path_list)
            for path in path_list:
                self.E.draw_path(path)

            print("Total Cost %.2f" % (cost))
            plt.show()
        #self.E.end_draw()

