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


    def draw_environment(self):
        plt.figure()
        plt.xlim(0, self.xmax)
        plt.ylim(0, self.ymax)
        plt.xticks(np.arange(0, self.xmax + 1, step=1))
        plt.yticks(np.arange(0, self.ymax + 1, step=1))
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
        plt.plot(xs, ys, color='r')

    def end_draw(self):
        plt.show()

# xmax, ymax = 22, 18
# start_point, end_point = (2, 2), (19, 16)
# polygon_point_list = np.array([[[4, 4], [5, 9], [8, 10], [9, 5]]
#                                       , [[8, 12], [8, 17], [13, 12]]
#                                       , [[11, 1], [11, 6], [14, 6], [14, 1]]
#                                       , [[12, 11], [14, 8], [15, 6], [19, 10]]])
# polygon_list_object = np.array([])
#
#
# for polygon_coord in polygon_point_list:
#     print(polygon_coord)
#     P = Polygon(polygon_coord)
#     polygon_list_object = np.append(polygon_list_object, [P])
#
# E = Environment(xmax, ymax, start_point, end_point, polygon_list_object)
#
# E.draw_environment()
#
# # path = np.array([[2, 2], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 4], [10, 5], [10, 6], [10, 7],
# #         [11, 8], [12, 9], [13, 10], [14, 11], [15, 12], [16, 13], [17, 14], [18, 15], [19, 16]])
# #
# # E.draw_path(path)
#
# plt.scatter(14, 11, color='r')
# plt.scatter(13, 10, color='r')
# E.end_draw()
#
# print("Testing valid move", E.is_valid_point((13, 10)))
# print("Testing valid move", E.is_valid_point((14, 11)))
# print("Testing valid move", E.is_valid_move((13, 10), (14, 11)))