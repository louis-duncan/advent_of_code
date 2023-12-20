from aoc_utils import *
import numpy as np
from PIL import Image
from pathlib import Path

from colour import Color

input_file = "test_input.txt"
grid = LineGrid(input_lines(input_file))
im_array = np.zeros([grid.width, grid.height, 3], dtype=np.uint8)
gradient = list(Color("green").range_to(Color("red"), 10))

for y in range(grid.width):
    for x in range(grid.height):
        im_array[y][x] = list(map(lambda v: 255 * v, gradient[int(grid.get(x, y))].get_rgb()))

img = Image.fromarray(im_array)
img.save(input_file.split(".")[0] + ".png")
