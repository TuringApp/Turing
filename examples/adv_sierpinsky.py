g_window(-10, 100, 100, -10)

order = 5
size = 2 ** order

for y in range(size):
    for x in range(size):
        if x & y == 0:
            g_point(x * 2, y * 2)