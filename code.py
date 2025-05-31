# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
# Fruit Jam DVI color checker
#
# The display color that gets output on DVI for each index of the
# displayio.Palette object depends on how the picodvi.Framebuffer gets
# initialized. The Palette class uses the most significant bits of each color,
# but the number of bits depends on the Framebuffer color_depth argument:
# - Framebuffer(..., color_depth=8):  3 bits red, 3 green, 2 blue
# - Framebuffer(..., color_depth=16): 5 bits red, 6 green, 5 blue
#
from board import BUTTON1, CKP, CKN, D0P, D0N, D1P, D1N, D2P, D2N
from digitalio import DigitalInOut, Direction, Pull
from displayio import (Bitmap, Group, OnDiskBitmap, Palette, TileGrid,
    release_displays)
from framebufferio import FramebufferDisplay
import gc
from picodvi import Framebuffer
import supervisor
from terminalio import FONT
from time import sleep

from adafruit_display_text import bitmap_label


def fill_palette(palette, style):
    # Fill the palette with 256 colors in the specified style
    if style == 'red':
        # 256 steps of red (dark to light)
        for i in range(256):
            palette[i] = (i, 0, 0)
    elif style == 'green':
        # 256 steps of green (dark to light)
        for i in range(256):
            palette[i] = (0, i, 0)
    elif style == 'blue':
        # 256 steps of blue (dark to light)
        for i in range(256):
            palette[i] = (0, 0, i)
    elif style == 'gray':
        # 256 steps of gray (dark to light)
        for i in range(256):
            palette[i] = (i, i, i)
    elif style == 'rgb332':
        # Full range of colors for 3 bits red, 3 bits green, and 2 bits blue
        i = 0
        for b in range(4):
            for g in range(8):
                for r in range(8):
                    palette[i] = (r << 5, g << 5, b << 6)
                    i += 1


# Configure Display Mode
RGB665 = False
if RGB665:
    COLOR_DEPTH = 16  # Use RGB665 palette colors
else:
    COLOR_DEPTH = 8   # Use RGB332 palette colors
release_displays()
gc.collect()
fb = Framebuffer(320, 240, clk_dp=CKP, clk_dn=CKN,
    red_dp=D0P, red_dn=D0N, green_dp=D1P, green_dn=D1N,
    blue_dp=D2P, blue_dn=D2N, color_depth=COLOR_DEPTH)
display = FramebufferDisplay(fb, auto_refresh=False)
supervisor.runtime.display = display
grp = Group(scale=1)
display.root_group = grp

# Make a bitmap + palette + tilegrid for 8-bit per pixel indexed color image
wide = 320
high = 240
bitmap = Bitmap(wide, high, 256)
palette = Palette(256)
tilegrid = TileGrid(bitmap, pixel_shader=palette)
grp.append(tilegrid)

# Fill bitmap with a grid of squares, one square for each color of the palette.
# This will end up looking like rectangles rather than squares though, because
# the palette colors get quantized by the pixel shader (or maybe picodvi?).
#
rows = 16
cols = 16
scale = 14
for y in range(rows * scale):
    base = (y // scale) * cols
    for x in range(cols * scale):
        c = base + (x // scale)
        bitmap[x, y] = c

# Cycle through the different palettes
while True:
    for style in ['red', 'green', 'blue', 'gray', 'rgb332']:
        fill_palette(palette, style)
        display.refresh()
        sleep(8)
