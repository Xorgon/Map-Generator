from matplotlib.path import Path
import numpy as np
import math


class Region():
    v_points = None
    d_point = None
    lines = None
    color = None
    fill_points = None

    def __init__(self):
        self.v_points = []
        self.lines = []
        self.fill_points = []

    def get_centroid(self):
        if len(self.v_points) == 0:
            return None
        x_sum = 0
        y_sum = 0
        for point in self.v_points:
            x_sum += point.x
            y_sum += point.y
        x_avg = x_sum / len(self.v_points)
        y_avg = y_sum / len(self.v_points)
        return x_avg, y_avg

    def contains_point(self, coords):
        point_coords = []
        for point in self.v_points:
            point_coords.append(point.get_tuple())
        if len(point_coords) == 0:
            return False
        point_coords = np.array(point_coords)
        path = Path(point_coords)
        return path.contains_point(coords)

    def set_colors(self, color):
        for v_point in self.v_points:
            v_point.color = color
        for line in self.lines:
            line.color = color
        self.d_point.color = color
        self.color = color

    def get_min(self):
        x = 9001
        y = 9001
        for p in self.v_points:
            if p.x < x:
                x = math.ceil(p.x)
            if p.y < y:
                y = math.ceil(p.y)
        return x, y

    def get_max(self):
        x = -1
        y = -1
        for p in self.v_points:
            if p.x > x:
                x = math.floor(p.x)
            if p.y > y:
                y = math.floor(p.y)
        return x, y

    def get_neighbor_regions(self):
        regions = []
        for line in self.d_point.lines:
            other_point = line.get_other_point(self.d_point)
            if other_point.region is not None:
                regions.append(other_point.region)
        return regions

    def sort_fill_points(self):
        self.fill_points = sorted(self.fill_points, key=lambda p: p.y)