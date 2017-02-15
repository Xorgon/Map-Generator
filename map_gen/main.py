from map_gen import generator
from tkinter import *
from PIL import Image, ImageTk
from map_gen.util import draw_util


class MapGenerator():
    tk_master = Tk()
    gen = None
    canvas = None

    def __init__(self):
        height = generator.Generator.HEIGHT
        width = generator.Generator.WIDTH

        self.gen = generator.Generator()

        self.canvas = Canvas(self.tk_master, width=width, height=height)

        parchment = ImageTk.PhotoImage(Image.open("assets/parchment.jpg"))
        tree = ImageTk.PhotoImage(Image.open("assets/tree.png").resize((5, 8), Image.ANTIALIAS))
        hill = ImageTk.PhotoImage(Image.open("assets/hill.png").resize((20, 13), Image.ANTIALIAS))
        mountain = ImageTk.PhotoImage(Image.open("assets/mountain.png").resize((40, 25), Image.ANTIALIAS))

        self.canvas.create_image(0, 0, image=parchment, anchor=NW)

        # for v_line in self.gen.v_lines:
        #     if v_line.color:
        #         draw_util.draw_line(self.canvas, v_line)

        for region in self.gen.regions:
            if region.color == "blue" and len(region.v_points) > 0:
                draw_util.draw_region_with_color(self.canvas, region, "#dcdcdc")
            if region.color:
                #if len(region.fill_points) == 0:
                    #draw_util.draw_region(self.canvas, region)
                for point in region.fill_points:
                    if point.color == "green":
                        self.canvas.create_image(point.x - 2.5, point.y - 4, image=tree, anchor=NW)
                    elif point.color == "brown":
                        self.canvas.create_image(point.x - 10, point.y - 6.5, image=hill, anchor=NW)
                    else:
                        draw_util.draw_point(self.canvas, point)

        for m in self.gen.mountains:
            for point in m.fill_points:
                self.canvas.create_image(point.x - 20, point.y - 12.5, image=mountain, anchor=NW)

        # for water in self.gen.waters:
        #     draw_util.draw_polygon(self.canvas, water.outline_points, "black")

        # draw_util.draw_polygon(self.canvas, self.gen.waters[0].outline_points, "black")

        # for line in self.gen.d_lines:
        #     draw_util.draw_line(self.canvas, line)

        # for line in self.gen.v_lines:
        #     draw_util.draw_line_with_color(self.canvas, line, "purple")

        # for point in self.gen.d_points:
        #     draw_util.draw_point(self.canvas, point)


        for line in self.gen.v_lines:
            if line.color == "blue":
                draw_util.draw_line_with_color(self.canvas, line, "#483320")


        # DEBUG
        for line in self.gen.v_lines:
            if line.color == "purple":
                draw_util.draw_line(self.canvas, line)
        for line in self.gen.d_lines:
            if line.color == "purple":
                draw_util.draw_line(self.canvas, line)
        for point in self.gen.v_points:
            if point.color == "purple":
                draw_util.draw_point(self.canvas, point)
        for point in self.gen.d_points:
            if point.color == "purple":
                draw_util.draw_point(self.canvas, point)

        self.canvas.pack()

        self.tk_master.mainloop()


test = MapGenerator()
