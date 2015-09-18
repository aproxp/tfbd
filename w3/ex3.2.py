"""
Write a script that reads in this list of points (x,y), fits/interpolates them with a polynomial of degree 3.
 Solve for the (real) roots of the polynomial numerically using Scipy’s optimization functions
 (not the root function in Numpy).
"""
__author__ = 'kmalarski'

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

# print(X, Y)

poly = numpy.polyfit(x, y, 3)

root = scipy.optimize.root(poly, 0)


print(poly)
# print(points[0][1])

