from enum import Enum


class Type(Enum):
    red = 1
    black = 2


class Line:
    point1 = None
    point2 = None
    regions = None
    color = None
    name = None

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.regions = []

    def __str__(self):
        name = "line"
        if self.name:
            name = self.name
        out = name
        if self.point1: out += ", " + str(self.point1)
        if self.point2: out += ", " + str(self.point2)
        if self.color: out += ", " + self.color
        return out

    def get_vector(self):
        return self.point1.x - self.point2.x, self.point1.y - self.point2.y

    def get_vector_with_start(self, start_p):
        if start_p == self.point1:
            return self.point2.x - self.point1.x, self.point2.y - self.point1.y
        else:
            return self.point1.x - self.point2.x, self.point1.y - self.point2.y

    def get_other_point(self, point):
        if point == self.point1:
            return self.point2
        elif point == self.point2:
            return self.point1
        else:
            return None

    def get_other_region(self, region):
        if region == self.regions[0]:
            return self.regions[1]
        elif region == self.regions[1]:
            return self.regions[0]
        else:
            return None
