#!/usr/bin/python3

import json
__author__ = 'aproxp'

rt_ary = []

with open('pizza-train') as data_file:
    data = json.load(data_file)
    for entry in data:
        rt_ary.append(entry["request_text"])

print(rt_ary[0])