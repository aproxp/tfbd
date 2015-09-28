#!/usr/bin/python3

__author__ = 'aproxp'

from sklearn import datasets, svm, metrics
import matplotlib.pyplot as plt

iris = datasets.load_iris()
digits = datasets.load_digits()

# print(digits.data)

clf = svm.SVC(gamma = 0.001, C = 100.)

print(digits.data[1])
print(digits.target[1])
clf.fit(digits.data[:-1], digits.target[:-1])
clf.predict(digits.data[:-1])

zip