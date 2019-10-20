"""
    Define Environment with Limit of (x,y), Polygons, start / end point.
    Draw the whole Environment with matplotlib.
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from object import Polygon

class Environment():
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list, place):
        self.xmax = xmax
        self.ymax = ymax
        self.start_point = start_point
        self.end_point = end_point
        self.polygon_list = polygon_list
        self.place = place;

    def is_valid_point(self, point):
        x, y = point
        if ((x <= 0) | (y <= 0) | (x >= self.xmax) | (y >= self.ymax)):
            return False
        for polygon in self.polygon_list:
            if polygon.is_inside(point) == True:
                return False

        return True

    def is_valid_move(self, p0, p1):
        for polygon in self.polygon_list:
            if (polygon.is_cut(p0, p1) == True): #If There is a polygon that cut (p0, p1) line => False move
                return False
        return True


    def draw_environment(self, a_id):
        plt.figure(a_id)
        plt.xlim(0, self.xmax)
        plt.ylim(0, self.ymax)
        plt.xticks(np.arange(0, self.xmax + 1, step=1))
        plt.yticks(np.arange(0, self.ymax + 1, step=1))
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')

        for polygon in self.polygon_list:
            polygon.draw()

    def draw_place(self):
        for (i, point) in enumerate(self.place):
            plt.scatter(point[0], point[1], c='r')
            mk = "$" + str(i) + "$"
            plt.scatter(point[0], point[1] + 0.5, marker=mk, c='r')

    def draw_path(self, path):
        xs, ys = zip(*path)
        plt.plot(xs, ys)
