__author__ = 'aproxp'

def test_fun():
    summation = 0
    for i in range(500):
        for j in range(1, 10001):
            summation += 1 / j * j
    return summation

import datetime

a = datetime.datetime.now()
result = test_fun()
b = datetime.datetime.now()
print("Result: {}".format(result))
print("Execution time: {}".format(b-a))
