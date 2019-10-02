from algorithm import Algorithm
from object import distance
import time
import heapq
import numpy as np

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

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
            # for p in trace_path:
            #     print(p)
            # print(trace_path)

            return np.array(trace_path)



    def run(self):
        time_start = time.time()
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
                    if ((self.fre[next_p] == 1) & (self.f[next_p] > self.d[p] + w_move + self.h[next_p])):
                        self.d[next_p] = self.d[p] + w_move
                        self.f[next_p] = self.d[p] + w_move + self.h[next_p]
                        heapq.heappush(pq, (self.f[next_p], next_p))
                        self.trace[next_p] = p
        self.cost = self.d[self.end_point]
        self.timeProcessing = (time.time() - time_start)

