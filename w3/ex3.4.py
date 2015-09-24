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


def make_target_list(data, parameter):
    target_list = []
    if parameter == 'giver_username_if_known':
        for dictionary in data:
            target_list.append([0] if dictionary[parameter] == "N/A" else [1])
    else:
        for dictionary in data:
            target_list.append(0 if dictionary[parameter] is False else 1)
    return target_list


def update_count_list(input_text, bag, count_list, text_index):
    for temp in input_text.split():
        word = ''.join(ch for ch in temp if ch.isalpha() or ch == '\'')
        if word in bag:
            count_list[text_index][bag.index(word)] += 1


cur_text_index = 0
for dictionary in content:
    update_count_list(dictionary['request_text'], bow, cnt_list, cur_text_index)

    cur_text_index += 1

# print(cnt_list[0])
# print(cnt_list[-1])
ninety_percent_of = lambda x: x[0:int(0.9*len(x))]
ten_percent_of = lambda x: x[int(0.9*len(x)):]

ninety_percent_of_data = ninety_percent_of(content)
ten_percent_of_data = ten_percent_of(content)

training_set = ninety_percent_of(cnt_list)
target = make_target_list(ninety_percent_of_data, parameter='requester_received_pizza')
testing_set = ten_percent_of(cnt_list)
actual_results = make_target_list(ten_percent_of_data, parameter='requester_received_pizza')

from sklearn import linear_model

log_regr = linear_model.LogisticRegression()
result = log_regr.fit(X=training_set, y=target)
resultat = log_regr.predict(X=testing_set)

def verify_accuracy(resultat, actual_results):
    agr_cnt = 0
    for i in range(len(resultat)):
        if resultat[i] == actual_results[i]:
            agr_cnt += 1

    print("Agreement percentage: {}% ".format(agr_cnt/len(actual_results) * 100))

verify_accuracy(resultat, actual_results)

training_set2 = make_target_list(ninety_percent_of_data, parameter='giver_username_if_known')
target_set2 = make_target_list(ninety_percent_of_data, parameter='requester_received_pizza')

result2 = log_regr.fit(X=training_set2, y=target_set2)
resultat2 = log_regr.predict(X=make_target_list(ten_percent_of_data, parameter='giver_username_if_known'))

verify_accuracy(resultat2, actual_results)
#
# no_usr_but_pizza = 0
# for dictionary in content:
#     if dictionary['giver_username_if_known'] == "N/A" and dictionary['requester_received_pizza'] == True:
#         no_usr_but_pizza += 1
# print(no_usr_but_pizza)

def get_info_about_givers(data):
    givers = []
    for dictionary in data:
        givers.append(1 if dictionary['giver_username_if_known'] != "N/A" else 0)
    return givers

extended_cnt_list = [[0] * (len(bow) + 1) for _ in range(len(content))]
cur_text_index = 0
for dictionary in content:
    update_count_list(dictionary['request_text'], bow, extended_cnt_list, cur_text_index)
    extended_cnt_list[cur_text_index][-1] = 0 if dictionary['giver_username_if_known'] != "N/A" else 1
    cur_text_index += 1

training_set3 = ninety_percent_of(extended_cnt_list)
testing_set3 = ten_percent_of(extended_cnt_list)
result3 = log_regr.fit(training_set3, target)
resultat3 = log_regr.predict(testing_set3)

verify_accuracy(resultat3, actual_results)