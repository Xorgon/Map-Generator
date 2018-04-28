from random import Random

from scipy.spatial import Voronoi, Delaunay
import numpy as np

import map_gen_2.util.vector_util as vect


class Generator:
    init_points = np.empty((0, 2))
    voronoi = None
    delaunay = None

    height = None
    width = None
    num_points = None
    rand = None

    water_dps = []
    water_polys = []
    water_points = []
    water_point_idxs = []
    water_edges = []

    debug_points = []

    def __init__(self, height=720, width=1280, num_points=1000, seed=None, regularity=2):

        self.height = height

        self.width = width
        self.num_points = num_points

        self.rand = Random()
        if seed is not None:
            self.rand.seed(seed)

        self.gen_random_init_points()

        self.delaunay = Delaunay(self.init_points)
        self.voronoi = Voronoi(self.init_points)

        for i in range(regularity):
            self.gen_centroid_init_points()
            self.delaunay = Delaunay(self.init_points)
            self.voronoi = Voronoi(self.init_points)

        for i in range(4):
            self.gen_water_points(500)
        for dps in self.water_dps:
            self.gen_water_polygon(dps)

        p1 = self.rand.randrange(0, num_points)
        p2 = self.get_delaunay_neighbours(p1)[0]
        line = self.get_shared_line(p1, p2)

    def gen_random_init_points(self):
        for i in range(self.num_points):
            self.init_points = np.insert(self.init_points, len(self.init_points),
                                         [self.rand.random() * self.width, self.rand.random() * self.height], axis=0)

    def gen_centroid_init_points(self):
        """ Generates initial points based on the centroids of the Voronoi diagram. """
        if self.voronoi is None:
            raise ValueError("Voronoi diagram is None")

        self.init_points = np.empty((0, 2))
        for region in self.voronoi.regions:
            if len(region) == 0:
                continue
            num_points = float(len(region))
            sum_coord = np.array([0.0, 0.0])
            for idx in region:
                if idx != -1:
                    sum_coord += self.voronoi.vertices[idx]
            coord = [sum_coord[0] / num_points, sum_coord[1] / num_points]

            self.init_points = np.insert(self.init_points, len(self.init_points), coord, axis=0)

    def grow_area_from_point(self, max_regions, init_point_idx):
        area_d_point_idxs = [init_point_idx]
        while len(area_d_point_idxs) < max_regions:
            area_d_point_idx = self.rand.choice(area_d_point_idxs)
            neighbour_idxs = self.get_delaunay_neighbours(area_d_point_idx)
            to_add = self.rand.choice(neighbour_idxs)
            if area_d_point_idxs.count(to_add) > 0:
                continue
            else:
                area_d_point_idxs.append(to_add)
        return area_d_point_idxs

    def get_delaunay_neighbours(self, point_idx):
        indices = self.delaunay.vertex_neighbor_vertices[0]
        indptr = self.delaunay.vertex_neighbor_vertices[1]
        neighbour_idxs = indptr[indices[point_idx]:indices[point_idx + 1]]
        return neighbour_idxs

    def get_shared_line(self, p1_idx, p2_idx):
        if p2_idx in self.get_delaunay_neighbours(p1_idx):
            points = []
            r1 = self.voronoi.regions[self.voronoi.point_region[p1_idx]]
            r2 = self.voronoi.regions[self.voronoi.point_region[p2_idx]]

            for v1 in r1:
                for v2 in r2:
                    if v1 == v2:
                        points.append(v1)
            return points

    def get_region_idxs_from_d_points(self, d_points):
        regions = []
        for p in d_points:
            regions.append(self.voronoi.point_region[p])
        return regions

    def gen_water_points(self, size):
        point = self.rand.randrange(0, len(self.init_points))
        d_points = self.grow_area_from_point(size, point)
        self.water_dps.append(d_points)
        self.water_point_idxs.extend(d_points)

    def gen_water_polygon(self, d_points):
        for d_p in d_points:
            self.water_points.append(self.delaunay.points[d_p])
            region_idx = self.voronoi.point_region[d_p]
            region = self.voronoi.regions[region_idx]
            region_poly = []

            edge_lines = []

            neighbours = self.get_delaunay_neighbours(d_p)
            for i in range(len(neighbours)):
                n = neighbours[i]
                if n not in self.water_point_idxs:
                    edge_lines.append(self.get_shared_line(d_p, n))

            for i in range(len(region)):
                v_idx = region[i]
                if v_idx == -1:
                    continue
                this_vert = self.voronoi.vertices[v_idx]
                next_i = i + 1
                if i + 1 == len(region):
                    next_i = 0
                expanded = False
                for line in edge_lines:
                    if v_idx in line and region[next_i] in line:
                        if region[next_i] == -1:
                            continue
                        next_vert = self.voronoi.vertices[region[next_i]]
                        line_segment = [this_vert, next_vert]
                        for s in range(3):
                            new_line_segment = []
                            for j in range(len(line_segment)):
                                new_line_segment.append(line_segment[j])
                                if j + 1 < len(line_segment):
                                    new_line_segment.append(
                                        vect.split_line(line_segment[j], line_segment[j + 1], self.rand))
                            line_segment = new_line_segment

                        self.water_edges.append(line_segment)
                        for vert in line_segment:
                            region_poly.append(vert)
                        expanded = True

                if not expanded:
                    region_poly.append(this_vert)

            self.water_polys.append(region_poly)
