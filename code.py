# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
from displayio import (Bitmap, Group, Palette, TileGrid, release_displays)
from framebufferio import FramebufferDisplay
import gc
from picodvi import Framebuffer
import supervisor
from terminalio import FONT

from adafruit_display_text import bitmap_label


def main():

    # Make sure display is configured for 320x240 8-bit
    display = supervisor.runtime.display
    if (display is None) or display.width != 320:
        print("Re-initializing display for 320x240")
        release_displays()
        gc.collect()
        fb = Framebuffer(320, 240, clk_dp=CKP, clk_dn=CKN,
            red_dp=D0P, red_dn=D0N, green_dp=D1P, green_dn=D1N,
            blue_dp=D2P, blue_dn=D2N, color_depth=8)
        display = FramebufferDisplay(fb)
        supervisor.runtime.display = display
    else:
        print("Using existing display")
    display.auto_refresh = False
    grp = Group(scale=2)
    display.root_group = grp
    display.refresh()

main()
