#!/usr/bin/python3

__author__ = 'aproxp'


def string_to_binary_array(x, padding):
    return [int(i) for i in "{0:b}".format(x).zfill(padding)]


num = int(input())
ary = []
for i in range(0, 2 ** num):
    ary.append(string_to_binary_array(i, num))

print(ary)
