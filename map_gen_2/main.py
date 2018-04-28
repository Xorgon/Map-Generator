from map_gen_2.canvas import MapCanvas
from map_gen_2.generator import Generator

height = 1090
width = 1920

gen = Generator(height, width, 7500, seed="1asnbn8569", regularity=3)
canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.show_map()
