from environment import Environment

WMAX = 1e3
dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

class Algorithm():
    def __init__(self, xmax, ymax, start_point, end_point, polygon_list):
        self.E = Environment(xmax, ymax, start_point, end_point, polygon_list)
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

    def imitate_environment(self):

        self.path = self.output()
        print("Time processing of A* : %.2f" % self.timeProcessing)
        print("Total cost : ", self.cost)
        self.E.draw_environment()
        if (len(self.path) != 0):
            self.E.draw_path(self.path)
        self.E.end_draw()
