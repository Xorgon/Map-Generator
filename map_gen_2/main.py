from map_gen_2.canvas import *
from map_gen_2.generator import Generator

height = 1080
width = 1920

gen = Generator(height, width, 10000, seed="fad53df832j5n", regularity=5)

# canvas = MapCanvasBasic(height, width)
canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.show_map()
