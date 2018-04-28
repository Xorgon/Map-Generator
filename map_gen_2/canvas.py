from tkinter import *
from PIL import Image, ImageTk
import math
from random import Random
import map_gen_2.util.vector_util as vect
from matplotlib.path import Path
import numpy as np


class MapCanvas:
    tk_master = None
    canvas = None
    rand = None

    height = None
    width = None

    # Assets
    parchment = None
    mountain = None
    tree = None
    hill = None

    def __init__(self, height=720, width=1280):
        self.tk_master = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.tk_master, width=width, height=height)
        self.rand = Random()
        self.rand.seed(0)

        self.load_assets()

    def load_assets(self):
        self.parchment = ImageTk.PhotoImage(Image.open("assets/parchment.jpg"))
        self.mountain = ImageTk.PhotoImage(Image.open("assets/mountain.png").resize((40, 25), Image.ANTIALIAS))
        self.tree = ImageTk.PhotoImage(Image.open("assets/tree.png").resize((5, 8), Image.ANTIALIAS))
        self.hill = ImageTk.PhotoImage(Image.open("assets/hill.png").resize((20, 13), Image.ANTIALIAS))

    def draw_line(self, p1, p2, color='black', width=1):
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=width)

    def draw_irregular_line(self, p1, p2, splits=3, mag_fact=0.25, color='black'):
        points = [p1, p2]
        for i in range(splits):
            new_points = []
            for p_idx in range(len(points)):
                new_points.append(points[p_idx])
                if p_idx + 1 < len(points):
                    new_points.append(vect.split_line(points[p_idx], points[p_idx + 1], self.rand, mag_fact))
            points = new_points

        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=color)

    def draw_multi_line(self, points, color='black', width=1):
        for i in range(len(points) - 1):
            self.draw_line(points[i], points[i + 1], color=color, width=width)

    def draw_point(self, p, color='black', radius=3):
        self.canvas.create_oval(p[0] - radius, p[1] - radius, p[0] + radius, p[1] + radius, fill=color)

    def fill_region(self, points, color='blue'):
        corrected_points = []
        for p in points:
            corrected_points.append([p[0], p[1]])
        self.canvas.create_polygon(corrected_points, fill=color, stipple="gray50")

    def fill_region_with_image(self, points, image, step=5, rand=None, offset_fact=0.5):
        min_p = [self.width, self.height]
        max_p = [0, 0]

        for point in points:
            min_p[0] = min(min_p[0], point[0])
            min_p[1] = min(min_p[1], point[1])
            max_p[0] = max(max_p[0], point[0])
            max_p[1] = max(max_p[1], point[1])

        path = Path(points)

        fill_points = []
        for x in np.arange(min_p[0], max_p[0], step):
            for y in np.arange(min_p[1], max_p[1], step):
                if path.contains_point([x, y]):
                    fill_points.append([x, y])

        fill_points = sorted(fill_points, key=lambda p: p[1])

        for fill_point in fill_points:
            if rand is None:
                rand = Random()
            offset = [(rand.random() - 0.5) * step * offset_fact, (rand.random() - 0.5) * step * offset_fact]
            self.canvas.create_image(fill_point[0] + offset[0], fill_point[1] + offset[1], image=image, anchor=CENTER)

    def draw_all_mountains(self, gen, points_per_mountain=1):
        dps = []
        for m in gen.sorted_mountain_dps:
            dps.extend(m)

        points = []
        for d_p in dps:
            points.append(gen.delaunay.points[d_p])

        sorted_points = sorted(points, key=lambda p: p[1])
        for i in range(len(sorted_points)):
            if i % points_per_mountain != 0:
                continue
            p = sorted_points[i]
            self.canvas.create_image(p[0], p[1], image=self.mountain, anchor=CENTER)

    def draw_mountain_range(self, points, points_per_mountain=2):
        sorted_points = sorted(points, key=lambda p: p[1])
        for i in range(len(sorted_points)):
            if i % points_per_mountain != 0:
                continue
            p = sorted_points[i]
            self.canvas.create_image(p[0], p[1], image=self.mountain, anchor=CENTER)

    def draw_map(self, gen, debug=False):
        self.canvas.create_image(self.width / 2, self.height / 2, image=self.parchment, anchor=CENTER)

        # Water
        for water_poly in gen.water_polys:
            self.fill_region(water_poly, '#dcdcdc')

        for edge in gen.water_edges:
            for i in range(len(edge) - 1):
                self.draw_line(edge[i], edge[i + 1], "#483320", 3)

        # Mountains
        self.draw_all_mountains(gen, 1)

        # Hills
        for d_p in gen.hill_dps:
            region = gen.voronoi.regions[gen.voronoi.point_region[d_p]]
            points = []
            for vert_idx in region:
                points.append(gen.voronoi.vertices[vert_idx])
            self.fill_region_with_image(points, self.hill, 12, offset_fact=0.2)

        # Forests
        for d_p in gen.forest_dps:
            region = gen.voronoi.regions[gen.voronoi.point_region[d_p]]
            points = []
            for vert_idx in region:
                points.append(gen.voronoi.vertices[vert_idx])
            self.fill_region_with_image(points, self.tree)

        if debug:
            self.draw_debug_geometry(gen)

    def show_map(self):
        self.canvas.pack()
        self.tk_master.mainloop()

    def draw_debug_geometry(self, gen):
        for ridge in gen.voronoi.ridge_vertices:
            v1_idx = ridge[0]
            v2_idx = ridge[1]
            if v1_idx != -1 and v2_idx != -1:
                self.draw_line(gen.voronoi.vertices[v1_idx], gen.voronoi.vertices[v2_idx])

        for vert in gen.voronoi.vertices:
            self.draw_point(vert, "blue", 1)
        for point in gen.init_points:
            self.draw_point(point, "red", 1)
        for p in gen.all_water_dps:
            self.draw_point(gen.delaunay.points[p], "blue")

        for line in gen.sorted_mountain_dps:
            points = []
            for d_p in line:
                points.append(gen.delaunay.points[d_p])
            self.draw_multi_line(points, color="red")
        for point in gen.all_mountain_dps:
            self.draw_point(gen.delaunay.points[point], color="purple")

        for p in gen.debug_points:
            self.draw_point(p, "yellow")
