from map_gen_2.canvas import MapCanvas
from map_gen_2.generator import Generator

height = 1090
width = 1920

gen = Generator(height, width, 10000, seed="5a463zxzcvvt452uuii5533aa0000", regularity=3)
canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.show_map()
