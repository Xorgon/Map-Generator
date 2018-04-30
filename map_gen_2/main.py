from map_gen_2.canvas import *
from map_gen_2.generator import Generator

height = 1080
width = 1920

gen = Generator(height, width, 5000, seed="Ja9*877/*-+++4", regularity=3)

# canvas = MapCanvasBasic(height, width)
canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.show_map()
