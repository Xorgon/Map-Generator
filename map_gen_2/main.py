from map_gen_2.canvas import MapCanvas
from map_gen_2.generator import Generator

height = 720
width = 1280

gen = Generator(height, width, 10000, seed="212363264asdff", regularity=5)
canvas = MapCanvas(height, width)
canvas.draw_map(gen)
canvas.show_map()
