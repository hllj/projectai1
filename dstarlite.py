from algorithm import Algorithm
from object import distance
import time
import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]
# dx = [-1,0,1,0]
# dy = [0,-1,0,1]





class DStarLite(Algorithm):
    def __init__(self, start_point, end_point, ENV):
        super().__init__(start_point, end_point, ENV)
        self.speedChangeX = 1
        self.speedChangeY = 0
        self.xLeft = self.E.xmax
        self.yLeft = self.E.ymax
        self.xRight = 0
        self.yRight = 0
        self.numberOfPolygon = len(self.E.polygon_list)
        self.g = {}
        self.rhs = {}
        self.queue = []
        self.km = 0
        (self.xstart, self.ystart) = start_point
        for i in range(self.E.xmax + 1):
            for j in range(self.E.ymax + 1):
                self.g[(i, j)] = float('inf')
                self.rhs[(i, j)] = float('inf')

        self.rhs[self.end_point] = 0
        heapq.heappush(self.queue, self.calKey(end_point) + end_point)

        for xy in self.E.polygon_list[-1].coord:
            (x, y) = xy
            self.xLeft = min(self.xLeft, x)
            self.yLeft = min(self.yLeft, y)
            self.xRight = max(self.xRight, x)
            self.yRight = max(self.yRight, y)

        self.xRight += self.speedChangeX
        self.yRight += self.speedChangeY

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

    def calKey(self, id):
        return (min(self.g[id], self.rhs[id]) + self.heuristic((self.xstart, self.ystart), id) + self.km, min(self.g[id], self.rhs[id]))

    def topKey(self):
        if (len(self.queue) > 0):
            return self.queue[0][:2]
        return (float('inf'), float('inf'))

    def distance(self, a, b):
        global rate_change
        x1, y1 = a
        x2, y2 = b

        if (self.E.is_valid_move(a, b) == False):
            return float('inf')
        # kiem tra o trong polygon return inf
        if (self.E.is_valid_point(b) == False):
            return float('inf')
        return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

    def updateVertex(self, u):
        if (u != self.end_point):
            (x, y) = u
            for i in range(8):
                x_next = x + dx[i]
                y_next = y + dy[i]
                if (self.E.is_valid_point((x_next, y_next))):
                    self.rhs[u] = min(self.rhs[u], self.g[(x_next, y_next)] + self.distance(u, (x_next, y_next)))

        id_in_queue = (-1, -1, -1, -1)
        for i in self.queue:
            if (u == (i[2], i[3])):
                id_in_queue = i
                break
        if (id_in_queue != (-1, -1, -1, -1)):
            self.queue.remove(id_in_queue)

        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.queue, self.calKey(u) + u)

    def ComputeShortestPath(self):
        while (self.topKey() < self.calKey((self.xstart, self.ystart)) or self.rhs[(self.xstart, self.ystart)] != self.g[(self.xstart, self.ystart)]):
            k_old = self.topKey()
            u = heapq.heappop(self.queue)
            (x, y) = (u[2], u[3])
            if (k_old < self.calKey((x, y))):
                heapq.heappush(self.queue, self.calKey((x, y)) + (x, y))
            elif self.g[(x, y)] > self.rhs[(x, y)]:
                self.g[(x, y)] = self.rhs[(x, y)]
                for i in range(8):
                    x_next = x + dx[i]
                    y_next = y + dy[i]
                    if (self.E.is_valid_point((x_next, y_next))):
                        self.updateVertex((x_next, y_next))
            else:
                self.g[(x, y)] = float('inf')
                self.updateVertex((x, y))
                for i in range(8):
                    x_next = x + dx[i]
                    y_next = y + dy[i]
                    if (self.E.is_valid_point((x_next, y_next))):
                        self.updateVertex((x_next, y_next))

    def output(self):
        # if (self.trace[self.end_point] == -1):
        #     print("There is no path from {} to {}".format(self.start_point, self.end_point))
        #     return []
        # else:
        #     if (self.trace[self.end_point] == -1):
        #         print("There is no path from {} to {}".format(self.start_point, self.end_point))
        #         return []
        #     else:
        #         print('Path from {} to {}:'.format(self.start_point, self.end_point))
        #         trace_path = []
        #         while (self.start_point != self.end_point):
        #             trace_path.append(self.end_point)
        #             self.end_point = self.trace[self.end_point]
        #
        #         trace_path.append(self.start_point)
        #         print("Length path: ", len(trace_path) - 2)
        #         return np.array(trace_path)
        pass

    def run(self):
        xlast = self.xstart
        ylast = self.ystart
        plast = (xlast, ylast)
        self.ComputeShortestPath()

        fig = plt.figure()
        plt.xlim(0, self.E.xmax)
        plt.ylim(0, self.E.ymax)
        plt.xticks(np.arange(0, self.E.xmax + 1, step=1))
        plt.yticks(np.arange(0, self.E.ymax + 1, step=1))
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')

        self.draw_start_end()
        for polygon in self.E.polygon_list:
            p = polygon.draw()

        ratechange = 0
        movingPolygon = self.E.polygon_list[1]
        movingPolygonOld = movingPolygon
        p = plt.scatter(self.xstart, self.ystart)
        line = plt.plot((xlast, self.xstart), (ylast, self.ystart), color='r')

        while (self.xstart, self.ystart) != self.end_point:

            rhs_min = float('inf')
            x_next = -1
            y_next = -1
            d = np.random.randint(3, size=(2, 1))
            movingPolygon.erase()

            movingPolygon.update(d[0] - 1, d[1] - 1, self.E)
            for i in range(8):
                x = self.xstart + dx[i]
                y = self.ystart + dy[i]
                if self.E.is_valid_point((x, y)):
                    if self.distance((self.xstart, self.ystart), (x, y)) + self.g[(x, y)] < rhs_min:
                        x_next = x
                        y_next = y
                        rhs_min = self.distance((self.xstart, self.ystart), (x, y)) + self.g[(x, y)]

            if (x_next, y_next) == (-1, -1) or rhs_min == float('inf'): break
            self.xstart = x_next
            self.ystart = y_next



            # ratechange +=1
            movingPolygon.draw()
            # line.pop(0).remove()

            # line = plt.plot((xlast, self.xstart), (ylast, self.ystart), color='r')
            p.remove()
            p = plt.scatter(self.xstart, self.ystart)
            # plt.pause(1)
            # print("toa do {0} {1}".format(self.xstart,self.ystart))

            # CẬP NHẬT ĐA GIÁC Ở ĐÂY

            #----------------------
            #
            # movingPolygon = self.E.polygon_list[-1]
            # update
            for i in range(self.xLeft, self.xRight + 1):
                for j in range(self.yLeft, self.yRight + 1):
                    if self.E.is_valid_point((i, j)):
                        for k in range(4):
                            u = i + dx[k]
                            v = j + dy[k]
                            if u >= self.xLeft and u <= self.xRight and v >= self.yLeft and v <= self.yRight:
                                if movingPolygon.is_inside((u, v)) != movingPolygonOld.is_inside((u, v)):
                                    self.updateVertex((i, j))

            self.km = self.km + self.heuristic((xlast, ylast), (self.xstart, self.ystart))



            (xlast, ylast) = (self.xstart, self.ystart)



            plt.pause(0.3)

            # self.E.polygon_list[-1].draw()

            self.ComputeShortestPath()
            movingPolygonOld = movingPolygon
        # plt.show()



