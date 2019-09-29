"""
    Define Object in Environment: Polygon, Point; checking a Point is (not) in a Polygon or not.
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

EPS = 1e-9

def Heron(a, b, c):
    p = (a + b + c) / 2
    return np.sqrt(p * (p - a) * (p - b) * (p - c))

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

class Polygon():
    def __init__(self, coord)   :
        self.coord = coord
        self.n_coord = len(coord)

    def draw(self):
        point_list = self.coord
        point_list = np.append(point_list, [self.coord[0]], axis=0)
        # print(point_list)
        xs, ys = zip(*point_list)
        # plt.figure()
        plt.plot(xs, ys)

    def area(self):
        area_polygon = 0
        for i in range(0, self.n_coord - 1):
            d_1 = distance(self.coord[0], self.coord[i])
            d_2 = distance(self.coord[0], self.coord[i + 1])
            d_1_2 = distance(self.coord[i], self.coord[i + 1])
            area_polygon += Heron(d_1, d_2, d_1_2)

        return area_polygon

    def is_inside(self, p):
        x, y = p
        test_area = 0
        for i in range(0, self.n_coord):
            i_next = (i + 1) % self.n_coord
            d_1 = distance(p, self.coord[i])
            d_2 = distance(p, self.coord[i_next])
            d_1_2 = distance(self.coord[i], self.coord[i_next])
            test_area += Heron(d_1, d_2, d_1_2)

        if (np.abs(test_area - self.area()) <= EPS):
            return True
        else:
            return False

# plt.figure()
# plt.xlim(0, 20)
# plt.ylim(0, 18)
# plt.gca().set_aspect('equal', adjustable='box')
# coord_1 = np.array([[4, 4], [5, 9], [8, 10], [9, 5]])
# coord_2 = np.array([[8, 12], [8, 17], [13, 12]])
# coord_3 = np.array([[11, 1], [11, 6], [14, 6], [14, 1]])
#
# P1 = Polygon(coord_1)
# P2 = Polygon(coord_2)
# P3 = Polygon(coord_3)
#
# P1.draw()
# P2.draw()
# P3.draw()
#
# plt.show()