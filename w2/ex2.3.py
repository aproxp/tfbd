"""
Write a script that takes this file (from this Kaggle competition),
extracts the request_text field from each dictionary in the list,
and construct a bag of words representation of the string (string to count-list).
"""
__author__ = 'kmalarski'


import json

with open("/home/kmalarski/Desktop/DTU/bigdata/tfbd_w2/tfbd_w2/pizza-train.json") as file:
    content = json.loads(file.read())


def make_bow(data):
    """
    The function creates Bag Of Words, id est a list of distinct words found within request_text field of an input json.
    Moreover, a count list, filled with zeros, is initialised.
    :param data: all the dictionaries taken from input file
    :return: bag of words, count list
    """
    bow = []
    for dictionary in data:
        for word in dictionary['request_text'].split():
            if word not in bow:
                bow.append(''.join(ch for ch in word if ch.isalpha() or ch == '\''))
                # bow.append(word)
        for word in bow:
            if word == '':
                bow.remove(word)
    count_list = [[0] * len(bow) for _ in range(len(data))]
    return bow, count_list

bow, cnt_list = make_bow(content)


def update_count_list(input_text, bag, count_list, text_index):
    for temp in input_text.split():
        word = ''.join(ch for ch in temp if ch.isalpha() or ch == '\'')
        if word in bag:
            count_list[text_index][bag.index(word)] += 1

cur_text_index = 0
for dictionary in content:
    update_count_list(dictionary['request_text'], bow, cnt_list, cur_text_index)

    cur_text_index += 1

print(cnt_list[0])
print(cnt_list[-1])
