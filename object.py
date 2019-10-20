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

def is_same_side(a, b, x_t, y_t, p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    v_0 = -b * (x0 - x_t) + a * (y0 - y_t)
    v_1 = -b * (x1 - x_t) + a * (y1 - y_t)
    if v_0 * v_1 > 0:
        return True
    else:
        return False

class Polygon():
    def __init__(self, coord)   :
        self.coord = coord
        self.n_coord = len(coord)
        self.area = self.area_cal()
        plt = None

    def draw(self):
        point_list = self.coord
        point_list = np.append(point_list, [self.coord[0]], axis=0)
        # print(point_list)
        xs, ys = zip(*point_list)
        self.plt = plt.plot(xs, ys,color = 'g')


    def erase(self ):
        l = self.plt.pop(0)
        l.remove()



    def update(self,dx,dy,E,cur):
        t = self.coord
        xs,ys = cur
        points = []
        kt = True
        for i in self.coord :

            x,y = i
            for poly in E.polygon_list:
                if poly == self :
                    continue
                if poly.is_inside((x+dx,y+dy)):
                    return False
                if poly.is_cut((x,y),(x+dx,y+dy)) :
                    return  False

            points.append((x+dx,y+dy))
        # print("di chuyen ")
        # print(dx, dy)


        self.coord = points

        if self.is_inside(cur) or self.is_inside(E.end_point) :
            self.coord= t
            return  False
        else :
            return  True

    def area_cal(self):
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

        if (np.abs(test_area - self.area) <= EPS):
            return True
        else:
            return False

    def is_cut(self, p0, p1):
        x0, y0 = p0
        x1, y1 = p1
        cut_count = 0
        for i in range(0, self.n_coord):
            i_next = (i + 1) % self.n_coord
            xi, yi = self.coord[i]
            xi_next, yi_next = self.coord[i_next]
            t1 = is_same_side(x0 - x1, y0 - y1, x0, y0, self.coord[i], self.coord[i_next])
            t2 = is_same_side(xi - xi_next, yi - yi_next, xi, yi, p0, p1)
            if ((t1 == False) & (t2 == False)):
                cut_count += 1
        if (cut_count >= 2):
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