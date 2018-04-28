from random import Random

import math
import timeit

from time import localtime, gmtime, strftime
from scipy.spatial import Voronoi, Delaunay
import numpy as np

from map_gen.objects.line import Line
from map_gen.objects.mountain import Mountain
from map_gen.objects.point import Point
from map_gen.objects.region import Region
from map_gen.objects.water import Water
from map_gen.util import vector_util


class Generator:
    v_points = []
    v_lines = []
    regions = []
    d_points = []
    d_lines = []

    mountains = []
    waters = []

    HEIGHT = 910  # 455
    WIDTH = 1588  # 794
    POINTS = 3500
    MIN_RED = math.ceil(4 * POINTS / 750)
    MAX_RED = math.ceil(8 * POINTS / 750)
    REGULARITY_IMPROVEMENT = 1
    WATER_EDGE_IMPROVEMENT = 3
    MOUNTAIN_DENSITY = 60

    SEED = "abcdefg"
    rand = None

    def __init__(self):
        self.v_points = []
        self.v_lines = []
        self.d_points = []
        self.d_lines = []
        self.regions = []
        self.rand = Random()
        self.rand.seed(self.SEED)
        estimate = (990.91 / (2500 ** 1.8)) * self.POINTS ** 1.8
        print("Started generating with {0:d} points, seed '{1:s}', "
              "at {2:s}, approximate time remaining is {3:s}."
              .format(self.POINTS, self.SEED,
                      strftime("%H:%M:%S", localtime()),
                      strftime("%H:%M:%S", gmtime(estimate))))
        actual = timeit.timeit(self.generate, number=1)
        print("Finished generating after {0:s} seconds.".format(strftime("%H:%M:%S", gmtime(actual))))
        print("Estimate was {:s} off.".format(strftime("%H:%M:%S", gmtime(estimate - actual))))

    def generate(self):
        print("Generating Delaunay points...")
        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(self.gen_d_points, number=1)))

        print("Calculating Voronoi diagram...")

        def calc_voronoi():
            print("    %i iterations remaining..." % (self.REGULARITY_IMPROVEMENT + 1))
            self.v_points, self.v_lines, self.regions = self.gen_v(self.d_points)
            for i in range(self.REGULARITY_IMPROVEMENT):
                print("    %i iterations remaining..." % (self.REGULARITY_IMPROVEMENT - i))
                self.d_points = self.improve_regularity(self.regions)
                self.v_points, self.v_lines, self.regions = self.gen_v(self.d_points)

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(calc_voronoi, number=1)))

        print("Generating Delaunay lines...")
        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(self.gen_d_lines, number=1)))

        print("Generating water...")

        def gen_water():
            total_quota = math.ceil(self.POINTS * (1 / 3))
            small_quota = math.ceil(total_quota * (1 / 4))
            large_quota = total_quota - small_quota

            small_used = 0
            small = []
            while small_used < small_quota:
                size = self.rand.randint(1, math.ceil(self.POINTS / 400))
                if small_quota - small_used < size:
                    size = small_quota - small_used
                small_used += size
                small.append(size)

            large_used = 0
            large = []
            while large_used < large_quota:
                size = self.rand.randint(math.floor(large_quota / 3), math.ceil(large_quota / 2))
                if large_quota - large_used < size:
                    size = large_quota - large_used
                large_used += size
                large.append(size)

            for size in small:
                reg = self.rand.choice(self.regions)
                self.gen_water(reg, size)
            for size in large:
                reg = self.rand.choice(self.regions)
                self.gen_water(reg, size)

                # for i in range(math.ceil(0.75 * self.POINTS / 250)):
                #     self.gen_area("blue", math.pow(0.18, math.pow(250 / self.POINTS, 1 / 17)))

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(gen_water, number=1)))

        print("Generating mountains...")
        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(self.gen_mountains,
                                                                      number=self.rand.randint(self.MIN_RED,
                                                                                               self.MAX_RED))))

        print("Generating forests...")

        def gen_forests():
            for i in range(math.ceil(12 * self.POINTS / 250)):
                self.gen_area("green", math.pow(0.025, math.pow(250 / self.POINTS, 1 / 12)))

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(gen_forests, number=1)))

        print("Generating hills...")

        def gen_hills():
            for i in range(math.ceil(12 * self.POINTS / 250)):
                self.gen_area("brown", math.pow(0.0145, math.pow(250 / self.POINTS, 1 / 12)))

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(gen_hills, number=1)))

        print("Making points...")

        def make_points():
            self.gen_all_region_points(6, "green")
            self.gen_all_region_points(20, "brown")

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(make_points, number=1)))

        print("Outlining regions...")

        def outline_regions():
            self.outline_regions("blue")
            # self.outline_water()

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(outline_regions, number=1)))

        print("Improving water edges...")

        def improve_water_edges():
            print("    %i iterations remaining..." % (self.WATER_EDGE_IMPROVEMENT + 1))
            for i in range(self.WATER_EDGE_IMPROVEMENT):
                print("    %i iterations remaining..." % (self.WATER_EDGE_IMPROVEMENT - i))
                to_add = []
                for line in self.v_lines:
                    if line.color == "blue":
                        lines = self.split_line(line)
                        if lines is not None:
                            to_add.append(lines[0])
                            to_add.append(lines[1])
                for line in to_add:
                    self.v_lines.append(line)

        print("    Finished in {0:.2f} seconds.".format(timeit.timeit(improve_water_edges, number=1)))

    def gen_d_points(self):
        for i in range(self.POINTS):
            self.d_points.append(Point(math.floor(self.rand.random() * self.WIDTH),
                                       math.floor(self.rand.random() * self.HEIGHT)))

    def gen_d_lines(self):
        dela = Delaunay(self.points_as_np_array(self.d_points))
        verts = dela.points
        for simplex in dela.simplices:
            for i in simplex:
                for j in simplex:
                    if i == j:
                        continue
                    vert1 = verts[i]
                    vert2 = verts[j]
                    point1 = self.get_d_point_from_coords(vert1[0], vert1[1])
                    point2 = self.get_d_point_from_coords(vert2[0], vert2[1])
                    line = Line(point1, point2)

                    point1.lines.append(line)
                    point2.lines.append(line)

                    self.d_lines.append(line)

    def gen_v(self, d_points):
        """
        Generates Voronoi points, lines and regions for some points.
        :param d_points:
        :return: v_points, v_lines, regions
        """
        vor = Voronoi(self.points_as_np_array(d_points))

        line_segments = []
        for simplex in vor.ridge_vertices:
            simplex = np.asarray(simplex)
            if np.all(simplex >= 0):
                line_segments.append([(x, y) for x, y in vor.vertices[simplex]])

        ptp_bound = vor.points.ptp(axis=0)

        center = vor.points.mean(axis=0)
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0):
                i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

                t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[i] + direction * ptp_bound.max()

                line_segments.append([(vor.vertices[i, 0], vor.vertices[i, 1]),
                                      (far_point[0], far_point[1])])

        # Generate Point and Line Objects for the Voronoi diagram.
        v_points = []
        v_lines = []
        for vor_line in line_segments:
            point1 = Point(vor_line[0][0], vor_line[0][1])
            point2 = Point(vor_line[1][0], vor_line[1][1])
            line = Line(point1, point2)

            if self.get_v_point(point1, v_points):
                if point1.lines.count(line) == 0:
                    self.get_v_point(point1, v_points).lines.append(line)
                line.point1 = self.get_v_point(point1, v_points)
            else:
                v_points.append(point1)
                point1.name = str(len(v_points))
                if point1.lines.count(line) == 0:
                    point1.lines.append(line)

            if self.get_v_point(point2, v_points):
                if point2.lines.count(line) == 0:
                    self.get_v_point(point2, v_points).lines.append(line)
                line.point2 = self.get_v_point(point2, v_points)
            else:
                v_points.append(point2)
                point2.name = str(len(v_points))
                if point2.lines.count(line) == 0:
                    point2.lines.append(line)

            v_lines.append(line)
            line.name = str(len(v_lines))

        # Generate Region Objects
        regions = []
        vor_verts = vor.vertices
        for region in vor.regions:
            points = []
            for i in region:
                if i == -1:
                    continue
                # TODO: Change these to rectify after lines have been generated so that the point can be moved to the mean of the connected points' coords.
                p_x = vor_verts[i][0]
                p_y = vor_verts[i][1]
                # if p_x > self.WIDTH:
                #     p_x = self.WIDTH
                # elif p_x < 0:
                #     p_x = 0
                #
                # if p_y > self.HEIGHT:
                #     p_y = self.HEIGHT
                # elif p_y < 0:
                #     p_y = 0
                points.append(self.get_v_point_from_coords(p_x, p_y, v_points))

            lines = []
            for p1 in points:
                for p2 in points:
                    line = self.get_line_by_points(p1, p2, v_lines)
                    if lines.count(line) == 0:
                        if line:
                            lines.append(line)
            new_region = Region()
            new_region.v_points = points
            new_region.lines = lines
            regions.append(new_region)
            for d_point in d_points:
                if new_region.contains_point(d_point.get_tuple()):
                    new_region.d_point = d_point
                    d_point.region = new_region
            for line in lines:
                if line.regions.count(new_region) == 0:
                    line.regions.append(new_region)
            for point in points:
                point.region = new_region
        return v_points, v_lines, regions

    @staticmethod
    def points_as_np_array(points):
        array = np.array([[]]).reshape((0, 2))
        for p in points:
            array = np.append(array, [[p.x, p.y]], 0)
        return array

    def get_v_point(self, point, v_points):
        for p in v_points:
            if point.x == p.x and point.y == p.y:
                return p
        return None

    def get_v_point_from_coords(self, x, y, v_points):
        for p in v_points:
            if p.x == x and p.y == y:
                return p
        return None

    def get_d_point(self, point):
        for p in self.d_points:
            if point.x == p.x and point.y == p.y:
                return p
        return None

    def get_d_point_from_coords(self, x, y):
        for p in self.d_points:
            if p.x == x and p.y == y:
                return p
        return None

    def gen_mountains(self):
        mountain = Mountain()

        origin_p = self.d_points[self.rand.randint(0, len(self.d_points) - 1)]
        end_p = self.d_points[self.rand.randint(0, len(self.d_points) - 1)]

        vect = (end_p.x - origin_p.x, end_p.y - origin_p.y)

        start_p = origin_p

        line = None
        angle = 9001  # arbitrarily high
        for test_line in start_p.lines:
            other_point = test_line.get_other_point(start_p)
            if other_point.region is None:
                continue
            if other_point.color is not None and other_point.color != "red":
                continue
            skip = False
            for region in other_point.region.get_neighbor_regions():
                if region.color is not None:
                    skip = True
            if skip:
                continue
            test_angle = vector_util.angle(test_line.get_vector_with_start(start_p), vect)
            if test_angle < angle:
                line = test_line
                angle = test_angle

        if line is None:
            return

        line.point1.color = "red"
        line.point2.color = "red"
        line.color = "red"

        count = 0
        finished = False
        while start_p != end_p and not finished:
            mountain.points.append(start_p)
            if line.point1 == start_p:
                start_p = line.point2
            else:
                start_p = line.point1

            if start_p == end_p:
                break

            vect = (end_p.x - start_p.x, end_p.y - start_p.y)

            line2 = None  # start_p.get_random_line(self.rand)
            angle = 9001  # arbitrarily high
            for test_line in start_p.lines:
                other_point = test_line.get_other_point(start_p)
                if other_point.color is not None and other_point.color != "red":
                    continue
                skip = False
                if other_point.region is None:
                    continue
                for region in other_point.region.get_neighbor_regions():
                    if region.color is not None:
                        skip = True
                if skip:
                    continue
                test_angle = vector_util.angle(test_line.get_vector_with_start(start_p), vect)
                if test_angle < angle:
                    line2 = test_line
                    angle = test_angle
            if line2 is None:
                return
            other_p_color = line2.get_other_point(start_p).color
            line = line2
            mountain.lines.append(line)
            line.color = "red"
            line.point1.color = "red"
            line.point2.color = "red"
            if count > 0.5 * math.sqrt(self.POINTS):
                finished = True
            if other_p_color == "red":
                finished = True
            count += 1

        if mountain.points.count(end_p) == 0:
            mountain.points.append(end_p)

        for line in mountain.lines:
            p1 = line.point1
            p2 = line.point2
            vect_p1_p2 = [p2.x - p1.x, p2.y - p1.y]
            num_points = math.ceil(self.MOUNTAIN_DENSITY / math.sqrt(self.POINTS))
            for i in range(num_points):
                coords = [p1.x + i * vect_p1_p2[0] / num_points, p1.y + i * vect_p1_p2[1] / num_points]
                point = Point(coords[0], coords[1])
                point.region = self.get_region(coords)
                mountain.fill_points.append(point)

        mountain.sort_fill_points()
        self.mountains.append(mountain)

    def simplify_v_points(self):
        """
        Removes points that are extremely close together.
        :return:
        """
        to_remove = []
        for p1 in self.v_points:
            if to_remove.count(p1) > 0:
                continue
            for p2 in self.v_points:
                if p1 == p2:
                    continue
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                canvas_diag = math.sqrt(self.HEIGHT ** 2 + self.WIDTH ** 2)
                if dist < 0.01 * canvas_diag:
                    to_remove.append(p2)
        for p in to_remove:
            self.v_points.remove(p)

    def get_line_by_points(self, p1, p2, v_lines):
        for line in v_lines:
            # if (line.point1 == p1 or line.point2 == p1) and (line.point1 == p2 or line.point2 == p2):
            #     return line
            if line.point1 == p1 and line.point2 == p2:
                return line
            if line.point1 == p2 and line.point2 == p1:
                return line
        return None

    def improve_regularity(self, regions):
        d_points = []
        for region in regions:
            if region.get_centroid():
                centroid = region.get_centroid()
                d_points.append(Point(centroid[0], centroid[1]))
        return d_points

    def paint_rand_region(self, color):
        placed = False
        while not placed:
            x = self.rand.randint(50, self.WIDTH - 50)
            y = self.rand.randint(50, self.HEIGHT - 50)
            for region in self.regions:
                if region.contains_point((x, y)):
                    region.set_colors(color)
                    placed = True

    def gen_area(self, color, growth_probability):
        unused_regions = []
        for test_region in self.regions:
            if test_region.color is None and (test_region.d_point is None or test_region.d_point.color is None):
                unused_regions.append(test_region)

        test_region = None

        while test_region is None or test_region.d_point is None or test_region.d_point.color is not None:
            index = self.rand.randint(0, len(unused_regions) - 1)
            test_region = unused_regions[index]
            if color != "blue" and test_region.d_point is not None:
                for secondary_region in test_region.get_neighbor_regions():  # Get all the connected regions
                    if secondary_region.color == "blue":
                        test_region = None
        regions = []
        regions_set = []
        regions.append(test_region)
        iterations = 0
        while len(regions) > 0:
            iterations += 1
            to_add = []
            for region in regions:
                if region is None or region.d_point is None:
                    continue

                # Set values for already selected regions.
                region.color = color
                region.d_point.color = color
                regions_set.append(region)

                # Select more regions.
                for line in region.d_point.lines:  # Get all connected lines
                    next_point = line.get_other_point(region.d_point)  # Get connected point
                    if next_point.color is not None:  # Make sure it hasn't already been filled
                        continue
                    if next_point.region is not None:
                        skip = False
                        if color != "blue":
                            for secondary_region in next_point.region.get_neighbor_regions():  # Get all the connected regions
                                if secondary_region.color != "blue" and secondary_region != region:
                                    skip = True
                            if skip:
                                continue
                    if self.rand.random() < math.pow(growth_probability, 1 + iterations / 10):
                        r_to_add = self.get_region(next_point.get_tuple())
                        if to_add.count(r_to_add) == 0:
                            to_add.append(r_to_add)
            regions = to_add

        if color == "blue":
            water = Water()
            water.regions = regions_set
            self.waters.append(water)

    def get_region(self, coords):
        for region in self.regions:
            if region.contains_point(coords):
                return region
        return None

    def outline_regions(self, color):
        for line in self.v_lines:
            colored_regions = 0
            for region in line.regions:
                if region.color == color:
                    colored_regions += 1
                    color = region.color
            if colored_regions == 1:
                line.color = color

    def outline_water(self):
        chain = []
        for line in self.v_lines:
            if line.color == "blue":
                chain.append(line)
                break

        start_point = chain[0].point1
        track_point = None
        prev_line = chain[0]
        while track_point != start_point:
            if track_point is None:
                track_point = start_point
            for line in track_point.lines:
                if line.color == "blue" and line != prev_line:
                    chain.append(line)
                    prev_line = line
                    track_point = line.get_other_point(track_point)
                    break
        for line in chain:
            line.color = "purple"

    def gen_all_region_points(self, spacing, color):
        for region in self.regions:
            if region.color == color:
                points_added = 0
                get_min = region.get_min()
                get_max = region.get_max()
                for x in range(get_min[0], get_max[0], spacing):
                    for y in range(get_min[1], get_max[1], spacing):
                        if region.contains_point((x, y)):
                            dx = 0.5 * self.rand.random() * spacing
                            dy = 0.5 * self.rand.random() * spacing
                            points_added += 1
                            point = Point(x + dx, y + dy)
                            point.region = region
                            point.color = color
                            region.fill_points.append(point)
                if points_added == 0:
                    region.d_point.color = color
                    region.fill_points.append(region.d_point)
                region.sort_fill_points()

    def split_line(self, line):
        p1 = line.point1
        p2 = line.point2
        line_vect = [p2.x - p1.x, p2.y - p1.y]
        unit_perp = vector_util.get_unit_perp(line_vect)
        if unit_perp is None:
            return
        line_mid = [p1.x + 0.5 * line_vect[0], p1.y + 0.5 * line_vect[1]]
        offset = np.multiply(0.25 * (self.rand.random() - 0.5) * vector_util.length(line_vect), unit_perp)
        new_point_coords = np.add(line_mid, offset)
        new_point = Point(new_point_coords[0], new_point_coords[1])
        new_point.color = line.color

        self.v_points.append(new_point)

        new_line_1 = Line(p1, new_point)
        new_line_1.color = line.color
        new_line_1.regions = line.regions

        new_line_2 = Line(new_point, p2)
        new_line_2.color = line.color
        new_line_2.regions = line.regions

        self.v_lines.remove(line)

        for region in line.regions:
            region.lines.remove(line)
            region.lines.append(new_line_1)
            region.lines.append(new_line_2)

            p_1_idx = region.v_points.index(p1)
            p_2_idx = region.v_points.index(p2)
            if p_1_idx > p_2_idx:
                if p_1_idx == len(region.v_points) - 1 and p_2_idx == 0:
                    region.v_points.append(new_point)
                else:
                    region.v_points.insert(p_1_idx, new_point)
            else:
                if p_2_idx == len(region.v_points) - 1 and p_1_idx == 0:
                    region.v_points.append(new_point)
                else:
                    region.v_points.insert(p_2_idx, new_point)

        return new_line_1, new_line_2

    def gen_water(self, start_region, max_regions):
        regions = []
        regions_set = []
        regions.append(start_region)
        while len(regions_set) < max_regions and len(regions) > 0:
            to_add = []
            for region in regions:
                if region is None or region.d_point is None:
                    continue

                # Set values for already selected regions.
                region.color = "blue"
                region.d_point.color = "blue"
                regions_set.append(region)
                # Select more regions.
                for line in region.d_point.lines:  # Get all connected lines
                    next_point = line.get_other_point(region.d_point)  # Get connected point
                    if next_point.color is not None:  # Make sure it hasn't already been filled
                        continue
                    r_to_add = self.get_region(next_point.get_tuple())
                    if len(regions_set) + len(to_add) < max_regions:
                        if to_add.count(r_to_add) == 0:
                            to_add.append(r_to_add)
            regions = to_add
        water = Water()
        water.regions = regions_set
        self.waters.append(water)

    def gen_river(self):
        # Start with a water edge
        # Find out if it spikes away from the water.
        # Choose a mountain and aim for it.
        # Keep going until you hit water or a different mountain.
        return
