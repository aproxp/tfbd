points = []

with open("/home/kmalarski/Desktop/DTU/bigdata/list.txt") as file:
    for line in file:
        points.append(line.strip().split(' '))

import numpy
import scipy.optimize

X = [float(points[i][0]) for i in range(len(points))]
Y = [float(points[i][1]) for i in range(len(points))]
x = numpy.array(X)
y = numpy.array(Y)

poly = numpy.polyfit(x, y, 3)


def f(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

root = scipy.optimize.root(f, 8, args=(poly[0], poly[1], poly[2], poly[3]))

print(root)

