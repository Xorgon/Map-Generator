from tkinter import *
from PIL import Image, ImageTk
import math
from random import Random
import map_gen_2.util.vector_util as vect


class MapCanvas:
    tk_master = None
    canvas = None
    rand = None

    height = None
    width = None

    # Assets
    parchment = None

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

    def draw_point(self, p, color='black', radius=3):
        self.canvas.create_oval(p[0] - radius, p[1] - radius, p[0] + radius, p[1] + radius, fill=color)

    def draw_region(self, points, color='blue'):
        corrected_points = []
        for p in points:
            corrected_points.append([p[0], p[1]])
        self.canvas.create_polygon(corrected_points, fill=color, stipple="gray50")

    def draw_map(self, gen, debug=False):
        self.canvas.create_image(self.width / 2, self.height / 2, image=self.parchment, anchor=CENTER)

        # Water
        for water_poly in gen.water_polys:
            self.draw_region(water_poly, '#dcdcdc')

        for edge in gen.water_edges:
            for i in range(len(edge) - 1):
                self.draw_line(edge[i], edge[i + 1], "#483320", 3)

        # Shows full geometry for debugging.
        if debug:
            for ridge in gen.voronoi.ridge_vertices:
                v1_idx = ridge[0]
                v2_idx = ridge[1]
                if v1_idx != -1 and v2_idx != -1:
                    self.draw_line(gen.voronoi.vertices[v1_idx], gen.voronoi.vertices[v2_idx])

            for vert in gen.voronoi.vertices:
                self.draw_point(vert, "blue", 1)
            for point in gen.init_points:
                self.draw_point(point, "red", 1)
            for p in gen.water_points:
                self.draw_point(p, "blue")

            for p in gen.debug_points:
                self.draw_point(p, "yellow")

    def show_map(self):
        self.canvas.pack()
        self.tk_master.mainloop()
