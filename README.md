<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2025 Sam Blenny -->
# Fruit Jam Gamepad Tester

**DRAFT: WORK IN PROGRESS**

Goal: Match 8-bit RGB colors from Fruit Jam DVI output with 24-bit sRGB or P3
colors on a computer.

This code was developed and tested on a pre-release revision B Fruit Jam
prototype board using CircuitPython 10.0.0-alpha builds from the
circuitpython.org
[Fruit Jam downloads](https://circuitpython.org/board/adafruit_fruit_jam/) page.
Things may change by the time CircuitPython 10.0.0 is released.


## Screen Captures at 8-bit Color Depth

These screenshots were taken with an EVGA XR1 Lite into macOS on a display set
for sRGB. The CircuitPython code was set to use `color_depth=8` for the
`framebufferio.FramebufferDisplay`. The result is that the palette colors get
quantized from 256 step ramps into just 4 or 8 values (RGB332). As you can see,
the color selection is okay for shades of green, blue, red, and magenta. But,
the grays and other hues aren't that great.


### Red (3 bits, 8 values)
![8-bit red palette](png/8-bit-red.png)


### Green (3 bits, 8 values)
![8-bit green palette](png/8-bit-green.png)


### Blue (2 bits, 4 values)
![8-bit blue palette](png/8-bit-blue.png)


### Gray (8 values but weird)

This one looks strange because blue is not able to change at the same rate as
red and green.

![8-bit gray palette](png/8-bit-gray.png)


### RGB332 Colors
![8-bit rgb332 palette](png/8-bit-rgb332.png)
