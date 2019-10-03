"""
TODO:
    - Create Algorithm Class with methods : input, output (path), run
    - Create 3 algorithms A-star, BFS, UCS that inherit from Algorithm Class
    - Use Environment Class to draw and check the valid moves.
"""
from __future__ import print_function
from object import Polygon
from environment import Environment
from ucs import UCS
from astar import ASTAR
from bfs import BFS

import time

import numpy as np


if __name__ == '__main__':
    file = open("input.txt", "r")
    all_content = file.readlines()

    xmax, ymax = map(int, all_content[0].split(','))

    a = list(map(int, all_content[1].split(',')))

    start_point = (a[0], a[1])
    end_point = (a[2], a[3])

    place = []
    for i in range(4, len(a), 2):
        place.append((a[i], a[i + 1]))

    polygon_point_list = []
    n = int(all_content[2])

    for i in range(n):
        polygon_point_list.append([])
        list_node = list(map(int, all_content[3 + i].split(',')))
        for j in range(0, len(list_node), 2):
            u = list_node[j]
            v = list_node[j + 1]
            polygon_point_list[i].append((u, v))

    file.close()

    polygon_list_object = np.array([])

    for polygon_coord in polygon_point_list:
        print(polygon_coord)
        P = Polygon(polygon_coord)
        polygon_list_object = np.append(polygon_list_object, [P])

    Env = Environment(xmax, ymax, start_point, end_point, polygon_list_object, place)

    time_start = time.time()
    AstarAlgo = ASTAR(start_point, end_point, Env)
    AstarAlgo.run()
    print("Time processing of A* : %.2f" % (time.time() - time_start))

    time_start = time.time()
    UCSAlgo = UCS(start_point, end_point, Env)
    UCSAlgo.run()
    print("Time processing of UCS : %.2f" % (time.time() - time_start))

    time_start = time.time()
    BFSAlgo = BFS(start_point, end_point, Env)
    BFSAlgo.run()
    print("Time processing of BFS : %.2f" % (time.time() - time_start))