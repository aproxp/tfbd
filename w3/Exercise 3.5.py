# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Exercise 3.5

# <rawcell>

# Write a simple Python function for computing the sum \frac{1}{1^2} + \frac{1}{2^2} + \frac{1}{3^2} + \ldots with 10,000 terms (this should be around 1.644), 500 times in a row (to make the execution time measurable). Now compile the code with Cython and see how much speedup you can achieve by this.

# <headingcell level=2>

# Python funtion:

# <codecell>

def test_fun():
    summation = 0
    for j in range(1, 10001):
        summation += 1 / (j * j)
    return summation

# <headingcell level=2>

# Cython:

# <codecell>

%load_ext cythonmagic

# <codecell>

%%cython
def test_cfun():
    cdef double summation,
    cdef int i, j
    
    summation = 0
    
    for j in range(1, 10001):
        summation += 1.0 / (j * j)
    return summation

# <headingcell level=2>

# Tests:

# <codecell>

test_fun()

# <codecell>

test_cfun()

# <codecell>

%%timeit
for _ in range(500):
    test_fun()

# <codecell>

%%timeit
for _ in range(500):
    test_cfun()

# <codecell>


