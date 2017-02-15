from tkinter import *
from PIL import Image, ImageTk


def draw_point(canvas, point):
    canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill=point.color)


def draw_line(canvas, line):
    canvas.create_line(line.point1.x, line.point1.y, line.point2.x, line.point2.y, fill=line.color, smooth=1)


def draw_line_with_color(canvas, line, color):
    canvas.create_line(line.point1.x, line.point1.y, line.point2.x, line.point2.y, fill=color, width="1.5", smooth=1)


def draw_region(canvas, region):
    coords = []
    for point in region.v_points:
        coords.append([point.x, point.y])
    canvas.create_polygon(coords, fill=region.color, stipple="gray50")


def draw_polygon(canvas, points, color):
    coords = []
    for point in points:
        coords.append([point.x, point.y])
    canvas.create_polygon(coords, fill=color, stipple="gray50")


def draw_region_with_color(canvas, region, color):
    coords = []
    for point in region.v_points:
        coords.append([point.x, point.y])
    canvas.create_polygon(coords, fill=color, stipple="gray50")

# def draw_image(canvas, image, coords, size):
#     img = Image.open("assets/" + image)
#     if size is not None:
#         img.resize(size)
#
#     canvas.create_image(coords[0], coords[1], image=ImageTk.PhotoImage(img), anchor=CENTER)
