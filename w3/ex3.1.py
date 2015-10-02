"""
Write a script which reads a matrix from a file like this one and solves the linear matrix equation
Ax=b where b is the last column of the input-matrix and A is the other columns.
It is okay to use the solve()-function from numpy.linalg.
"""
__author__ = 'kmalarski'

import numpy

results = []
with open("matrix.txt") as inputfile:
    for line in inputfile:
        results.append(line.strip().split(','))

b = []
A = []
for row in range(len(results)):
    A.append([])
    b.append([])
    for col in range(len(results[row])):
        if col == len(results[row]) - 1:
            b[row].append(int(results[row][col]))
        else:
            A[row].append(int(results[row][col]))
b = numpy.array(b)
A = numpy.array(A)

result = numpy.linalg.solve(A, b)

print(result)