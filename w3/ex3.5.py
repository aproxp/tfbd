__author__ = 'kmalarski'

def summing_test():
    result = 0
    for j in range(500):
        for i in range(1, 10001):
            result += 1 / i * i
    return result

import datetime

a = datetime.datetime.now()
test = summing_test()
b = datetime.datetime.now()

print("THe sum equals: {}".format(test))
print("The operation took: {} microseconds.".format((b-a)))
