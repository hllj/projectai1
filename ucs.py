from algorithm import Algorithm
import heapq
import numpy as np
import time
import matplotlib.pyplot as plt

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

class UCS(Algorithm):
    def __init__(self, start_point, end_point, ENV):
        super().__init__(start_point, end_point, ENV)
        self.d = {}
        for i in range(self.E.xmax + 1):
            for j in range(self.E.ymax + 1):
                self.d[(i, j)] = WMAX
                self.fre[(i, j)] = 1
                self.trace[(i, j)] = -1

        self.d[self.start_point] = 0

    def output(self):
        if (self.trace[self.end_point] == -1):
            print("There is no path from {} to {}".format(self.start_point, self.end_point))
            return []
        else:
            trace_path = []
            while (self.start_point != self.end_point):
                trace_path.append(self.end_point)
                self.end_point = self.trace[self.end_point]

            trace_path.append(self.start_point)
            return np.array(trace_path)

    def run(self,mode = 1):
        plt.title("UCS Algorithm")
        time_start = time.time()
        pq = []
        heapq.heappush(pq, (0, self.start_point))
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
                    if ((self.fre[next_p] == 1) & (self.d[next_p] > self.d[p] + w_move)):
                        self.d[next_p] = self.d[p] + w_move
                        heapq.heappush(pq, (self.d[next_p], next_p))
                        self.trace[next_p] = p
                        if mode :
                            plt.plot((px, px + dx[i]), (py, py + dy[i]), color='r')
                            plt.pause(0.00000001)

        self.cost = self.d[self.end_point]
        self.timeProcessing = (time.time() - time_start)

        if mode >= 0:
            path = self.output()
            if (len(path) > 0):
                self.E.draw_path(path)
            # plt.show()
