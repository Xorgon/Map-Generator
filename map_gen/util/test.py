import math
from matplotlib.pyplot import plot

p_old = [100, 200, 300, 400, 500, 750, 1000, 1250, 1500, 2000, 2500, 5000, 10000]
t_old = [1.13, 4.51, 11.36, 19.04, 32.57, 68.37, 136.16, 227.42, 342.95, 604.32, 952.33, 4896.57, 19378.57]

p = [500, 1000, 1500, 2000, 2500, 3000, 3500, 5000]
t = [31.98, 108.24, 252.35, 653.00, 990.91, 1380.07, 1821.65, 3134.87]

def gen_exp():
    x = range(0, 10100, 100)
    y = []
    for this_x in x:
        y.append(37.23 * math.exp(this_x / 771.18))
    return x, y


def gen_poly(poly):
    x = range(0, p[-1] + 100, 100)
    y = []
    a = 990.91/(2500**poly)
    for this_x in x:
        # y.append(1.5237e-4 * math.pow(this_x, 2))
        y.append(a * this_x ** poly)
    return x, y


def plot_graph():
    x_y_exp = gen_exp()
    x_exp = x_y_exp[0]
    y_exp = x_y_exp[1]

    x_y_poly = gen_poly(1.65)
    x_poly = x_y_poly[0]
    y_poly = x_y_poly[1]

    plot(p, t, x_poly, y_poly)


plot_graph()
