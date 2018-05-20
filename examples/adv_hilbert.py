# http://www.fundza.com/algorithmic/space_filling/hilbert/basics/index.html

last_x, last_y = -1, -1

def add_point(x, y):
    global last_x, last_y
    
    if last_x != -1:
        g_line(last_x, last_y, x, y)
    
    last_x, last_y = x, y

def hilbert(x0, y0, xi, xj, yi, yj, n):
    if n <= 0:
        X = x0 + (xi + yi)/2
        Y = y0 + (xj + yj)/2
        
        add_point(X, Y)
    else:
        hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1)
        hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1)
    
g_window(0, 1, 0, 1)
hilbert(0, 0, 1, 0, 0, 1, 3)