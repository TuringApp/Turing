import colorsys
import numpy as np

g_window(-5, 5, -2, 2)

step = 0.2
size = 0.1

func = lambda a: 1.5 * cos(a) * cos(0.5 * a)

for x in np.arange(-5, 5, step):
    (r, g, b) = colorsys.hsv_to_rgb((x + 5) / 10, 1.0, 1.0)
    r = int(255 * r)
    g = int(255 * g)
    b = int(255 * b)
    clr = ('#%02x%02x%02x') % (r, g, b)
    
    for xx in np.arange(x, x + step + size, size):
        y = func(xx)
        g_line(xx, y, xx, 0, clr)