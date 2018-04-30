from map_gen_2.canvas import *
from map_gen_2.generator import Generator

width = 3840
height = 2160

# fad53df832j5n 3840, 2160, 25000, 5 Big central sea.

gen = Generator(height, width, 25000, seed="56htncfhdr'##43", regularity=5)

# canvas = MapCanvasBasic(height, width)
canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.show_map()
