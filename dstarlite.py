from algorithm import Algorithm
from object import distance
import time
import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from object import Polygon

dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]
d2x = [-1,0,1,0]
d2y = [0,-1,0,1]

class DStarLite(Algorithm):
    def __init__(self, start_point, end_point, ENV):
        super().__init__(start_point, end_point, ENV)
        self.numberOfPolygon = len(self.E.polygon_list)
        self.g = {}
        self.rhs = {}
        self.queue = []
        self.km = 0
        (self.xstart, self.ystart) = self.start_point

        for i in range(self.E.xmax + 1):
            for j in range(self.E.ymax + 1):
                self.g[(i, j)] = float('inf')
                self.rhs[(i, j)] = float('inf')

        self.rhs[self.end_point] = 0
        heapq.heappush(self.queue, self.calKey(self.end_point) + self.end_point)

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
        x1, y1 = a
        x2, y2 = b

        if (self.E.is_valid_point(b) == False or self.E.is_valid_point(a) == False):
            return float('inf')
        return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

    def updateVertex(self, u):
        if (u != self.end_point):
            (x, y) = u
            minRhs = float('inf')
            for i in range(8):
                x_next = x + dx[i]
                y_next = y + dy[i]
                if (x_next > 0 and x_next < self.E.xmax and y_next > 0 and y_next < self.E.ymax):
                    minRhs = min(minRhs, self.g[(x_next, y_next)] + self.distance(u, (x_next, y_next)))
            self.rhs[u] = minRhs

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
                    if 0 < x_next < self.E.xmax and 0 < y_next < self.E.ymax:
                        self.updateVertex((x_next, y_next))
            else:
                self.g[(x, y)] = float('inf')
                self.updateVertex((x, y))
                for i in range(8):
                    x_next = x + dx[i]
                    y_next = y + dy[i]
                    if 0 < x_next < self.E.xmax and 0 < y_next < self.E.ymax:
                        self.updateVertex((x_next, y_next))


    def scanForChange(self, movingPolygon, movingPolygonOld):
        updateQueue = {}
        count = 0
        for k in range(8):
            u = self.xstart + dx[k]
            v = self.ystart + dy[k]
            if 0 < u < self.E.xmax and 0 < v < self.E.ymax:
                updateQueue[count] = (u, v)
                count += 1

        rangeCheck = 1
        scanRange = 8
        while rangeCheck < scanRange:
            newQueue = {}
            cnt = 0
            for i in range(count):
                x, y = updateQueue[i]
                for k in range(8):
                    u = x + dx[k]
                    v = y + dy[k]
                    if 0 < u < self.E.xmax and 0 < v < self.E.ymax:
                        exsisted = False
                        for j in range(count):
                            if (u, v) == updateQueue[j]:
                                exsisted = True
                                break
                        if exsisted == False:
                            newQueue[cnt] = (u, v)
                            cnt += 1
            for i in range(cnt):
                exsisted = False
                for j in range(count):
                    if newQueue[i] == updateQueue[j]:
                        exsisted = True
                        break
                if exsisted == False:
                    updateQueue[count] = newQueue[i]
                    count += 1
            rangeCheck += 1

        costIsChange = False
        for i in range(count):
            x, y = updateQueue[i]
            for k in range(8):
                u = x + dx[k]
                v = y + dy[k]
                if 0 < u < self.E.xmax and 0 < v < self.E.ymax:
                    if movingPolygon.is_inside((u, v)) != movingPolygonOld.is_inside((u, v)):
                        self.updateVertex(updateQueue[i])
                        costIsChange = True
        return costIsChange

    def run(self):
        # np.random.seed(2)
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

        movingPolygon = self.E.polygon_list[1]
        movingPolygonOld = Polygon(movingPolygon.coord)
        p = plt.scatter(self.xstart, self.ystart)
        line = plt.plot((xlast, self.xstart), (ylast, self.ystart), color='r')

        while (self.xstart, self.ystart) != self.end_point:
            if self.g[(self.xstart, self.ystart)] == float('inf'):
                break

            rhs_min = float('inf')
            x_next = -1
            y_next = -1

            for i in range(8):
                x = self.xstart + dx[i]
                y = self.ystart + dy[i]
                if self.E.is_valid_point((x, y)):
                    if self.distance((self.xstart, self.ystart), (x, y)) + self.g[(x, y)] < rhs_min:
                        x_next = x
                        y_next = y
                        rhs_min = self.distance((self.xstart, self.ystart), (x, y)) + self.g[(x, y)]

            plt.plot((self.xstart, x_next), (self.ystart, y_next), color='r')

            self.xstart = x_next
            self.ystart = y_next

            movingPolygon.erase()
            cnt = 0
            while True:
                cnt += 1
                r = np.random.random(1)
                d = int(r[0] * 8) % 8
                if movingPolygon.update(dx[d], dy[d], self.E, (self.xstart, self.ystart)): break
                print("In while loop:", cnt)
            self.E.polygon_list[1] = movingPolygon

            movingPolygon.draw()
            p.remove()
            p = plt.scatter(self.xstart, self.ystart)

            # UPDATE COST CHANGED
            self.km = self.km + self.heuristic((xlast, ylast), (self.xstart, self.ystart))
            costIsChange = self.scanForChange(movingPolygon, movingPolygonOld)

            if costIsChange == False:
                self.km = self.km - self.heuristic((xlast, ylast), (self.xstart, self.ystart))
            else:
                (xlast, ylast) = (self.xstart, self.ystart)
                self.ComputeShortestPath()

            plt.pause(0.000001)
            movingPolygonOld = Polygon(movingPolygon.coord)
        plt.show()



