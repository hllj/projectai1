"""
TODO:
    - Create Algorithm Class with methods : input, output (path), run
    - Create 3 algorithms A-star, BFS, UCS that inherit from Algorithm Class
    - Use Environment Class to draw and check the valid moves.
"""
from __future__ import print_function
from object import Polygon
from ucs import UCS
from astar import ASTAR
from bfs import BFS
from route import Route


import numpy as np


if __name__ == '__main__':
    xmax, ymax = 22, 18
    start_point, end_point = (1, 1), (19, 16)
    polygon_point_list = np.array([[[4, 4], [5, 9], [8, 10], [9, 5]]
                                      , [[8, 12], [8, 17], [13, 12]]
                                      , [[11, 1], [11, 6], [14, 6], [14, 1]]
                                      , [[15, 11], [12, 9], [15, 6], [19, 10]]
                                    , [[2,3], [3,3],[4,0],[2,0]]])
    check_point_list = [(2, 7), (12, 17), (17, 2)]

    polygon_list_object = np.array([])

    for polygon_coord in polygon_point_list:
        print(polygon_coord)
        P = Polygon(polygon_coord)
        polygon_list_object = np.append(polygon_list_object, [P])


    AstarAlgo = ASTAR(xmax, ymax, start_point, end_point, polygon_list_object)
    AstarAlgo.run()
    AstarAlgo.imitate_environment()

    r =Route(xmax, ymax, start_point, end_point, polygon_list_object, check_point_list)
    print(r.matrix_cost)

    # time_start = time.time()
    # UCSAlgo = UCS(xmax, ymax, start_point, end_point, polygon_list_object)
    # UCSAlgo.run()
    # print("Time processing of UCS : %.2f" % (time.time() - time_start))
    #
    # time_start = time.time()
    # BFSAlgo = BFS(xmax, ymax, start_point, end_point, polygon_list_object)
    # BFSAlgo.run()
    # print("Time processing of BFS : %.2f" % (time.time() - time_start))