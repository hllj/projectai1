from algorithm import Algorithm
import queue
import numpy as np
import time
import matplotlib.pyplot as plt

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

class BFS(Algorithm):
    def __init__(self, start_point, end_point, ENV):
        super().__init__(start_point, end_point, ENV)
        for i in range(self.E.xmax + 1):
            for j in range(self.E.ymax + 1):
                self.fre[(i, j)] = 1
                self.trace[(i, j)] = -1

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
            print("Length path: ", len(trace_path) - 2)
            return np.array(trace_path)

    def run(self,mode = 1):
        plt.title("BFS Algorithm")
        time_start = time.time()
        Q = queue.Queue()
        Q.put(self.start_point)
        while (not Q.empty()):
            px, py = Q.get()
            if ((px, py) == self.end_point):
                break
            for i in range(8):
                next_p = (px + dx[i], py + dy[i])
                w_move = 1
                if ((self.E.is_valid_point(next_p) == True) & (self.E.is_valid_move((px, py), next_p))):
                    if self.fre[next_p] == 1:
                        self.fre[next_p] = 0
                        self.trace[next_p] = (px, py)
                        Q.put(next_p)
                        if mode :
                            plt.plot((px, px + dx[i]), (py, py + dy[i]), color='r')
                            plt.pause(0.00000001)
        self.timeProcessing = (time.time() - time_start)
        if mode >= 0:
            path = self.output()
            if (len(path) > 0):
                self.E.draw_path(path)
            # plt.show()

