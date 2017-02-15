from map_gen import generator as g


class Point:
    x = 0
    y = 0
    lines = []
    color = None
    name = None
    region = None

    def __init__(self, x, y):
        self.lines = []
        # TODO: Use a line to backtrace until it's in rather than just setting 0. Also fix other function using this.
        if x > g.Generator.WIDTH:
            self.x = g.Generator.WIDTH
        elif x < 0:
            self.x = 0
        else:
            self.x = x

        if y > g.Generator.HEIGHT:
            self.y = g.Generator.HEIGHT
        elif y < 0:
            self.y = 0
        else:
            self.y = y

    def get_tuple(self):
        return self.x, self.y

    def __str__(self):
        name = ""
        if name: name = self.name + ", "
        return name + "(" + str(self.x) + ", " + str(self.y) + ")"

    def is_edge(self):
        edge = False
        if self.x == 0 or self.x == g.Generator.WIDTH:
            edge = True
        if self.y == 0 or self.y == g.Generator.HEIGHT:
            edge = True
        return edge

    def get_random_line(self, rand):
        return self.lines[rand.randint(0, len(self.lines) - 1)]