#!/usr/bin/python3

import sys

def read_matrix(file_name):
    with open(file_name, 'r') as file:
        array = []
        array2 = file.readlines()
        array = [[int(i) for i in line.rstrip().split()] for line in array2]
        return array


def write_matrix(file_name2, array):
    with open(file_name2, 'w') as file:
        for i in array:
            for j in i:
                file.write(str(j) + ' ')
            file.write('\n')

file_name = str(sys.argv[1])
file_name2 = str(sys.argv[2])

print(str(read_matrix(file_name)))
write_matrix(file_name2, read_matrix(file_name))
