from environment import Environment
import matplotlib.pyplot as plt

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

class Algorithm():
    def __init__(self, start_point, end_point, ENV):
        self.E = ENV
        self.start_point = start_point
        self.end_point = end_point
        self.path = []
        self.fre = {}
        self.trace = {}
        self.timeProcessing = 0
        self.cost = 0
    def output(self):
        pass

    def run(self):
        pass


    def draw_start_end(self):
        plt.scatter(self.start_point[0], self.start_point[1])
        plt.scatter(self.start_point[0], self.start_point[1] + 0.5, marker="$S$")

        plt.scatter(self.end_point[0], self.end_point[1])
        plt.scatter(self.end_point[0], self.end_point[1] + 0.5, marker="$G$")

    def imitate_environment(self):
        self.E.draw_environment()
        self.draw_start_end()
        if (len(self.E.place) > 0):
            self.E.draw_place()
        self.path = self.output()
        if (len(self.path) != 0):
            self.E.draw_path(self.path)
        self.E.end_draw()
