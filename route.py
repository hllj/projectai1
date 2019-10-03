from environment import Environment
import numpy as np
from astar import ASTAR
from object import Polygon

WMax = float('INF')
class Route():
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list, check_point_list):
        self.E = Environment(xmax, ymax, start_point, end_point, polygon_list)
        self.start_point = start_point
        self.end_point = end_point
        self.path = []
        self.fre = {}
        self.trace = {}
        self.timeProcessing = 0
        self.cost = 0
        self.check_point_list = check_point_list

        n = len(self.check_point_list)
        self.matrix_cost = np.full((n, n), WMax)
        n = len(self.check_point_list)
        for i in range(n):
            for j in range(n):
                if i != j:
                    astarAlgo = ASTAR(xmax, ymax, self.check_point_list[i], self.check_point_list[j], polygon_list)
                    astarAlgo.run()
                    self.matrix_cost[i][j] = astarAlgo.cost
    def run(self):
        pass

