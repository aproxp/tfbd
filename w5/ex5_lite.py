"""
Tasks from week 5 for sql lite.
"""
__author__ = 'kmalarski'

import sqlite3 as lite

#5.1
print("5.1")
con = lite.connect('/home/kmalarski/Desktop/DTU/bigdata/tfbd/w5/northwind.db')
con.text_factory = lambda x: str(x, 'latin1')
cur = con.cursor()
with con:
    # some queries, just to confirm that we have connection
    cur.execute("SELECT LastName, FirstName FROM Employees")
    print(cur.fetchall())
    cur.execute("SELECT * FROM Employees WHERE EmployeeID = 1")
    print(cur.fetchone())
    cur.execute("SELECT FirstName FROM Employees ORDER BY FirstName ASC")
    print(cur.fetchall())

#5.2

print("5.2")
cur.execute('SELECT pr.ProductName, od.UnitPrice, od.Quantity, od.OrderID  FROM Products pr JOIN "Order Details" od ON pr.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID WHERE o.CustomerID = "ALFKI"')
results = cur.fetchall()
alfki_product_list = []  # this list will be needed for 5.7
cur_order_id = 0
for row in results:
    if row[-1] == cur_order_id:  # if it's still the same order, we go on printing...
        print("Product Name: {} Unit Price: {} Quantity: {} ".format(row[0], row[1], row[2]))
    else:  # ...unless it's new one - time to print new order number as well.
        print("Order number {}:".format(row[-1]))
        print("Product Name: {} Unit Price: {} Quantity: {} ".format(row[0], row[1], row[2]))
        cur_order_id = row[-1]
    alfki_product_list.append(row[0])

print()

#5.3
print("5.3")
cur.execute('SELECT pr.ProductName, od.UnitPrice, od.Quantity, od.OrderID FROM Products pr JOIN "Order Details" od ON pr.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID WHERE o.CustomerID = "ALFKI"')
results = cur.fetchall()
cur_order_id = 0
cur_order = []
for row in results:
    if row[-1] == cur_order_id:
        cur_order.append(row)
    else:
        if len(cur_order) > 1:
            print("Order number {}:".format(cur_order_id))
            for record in cur_order:
                print("Product Name: {} Unit Price: {} Quantity: {} ".format(record[0], record[1], record[2]))
        cur_order_id = row[-1]
        cur_order = [row]
if len(cur_order) > 1:
            print("Order number {}:".format(cur_order_id))
            for record in cur_order:
                print("Product Name: {} Unit Price: {} Quantity: {} ".format(record[0], record[1], record[2]))

#5.4
print("5.4")
cur.execute('SELECT e.FirstName, e.LastName FROM Employees e JOIN Orders o ON e.EmployeeID = o.EmployeeID JOIN "Order Details" od ON o.OrderID = od.OrderID JOIN Products p ON od.ProductID = p.ProductID WHERE p.ProductID = 7')
results = cur.fetchall()
people_dict = {}
how_many = 0
for record in results:
    person = record[0] + ' ' + record[1]  # e.g: John Smith
    if person not in people_dict.keys():
        people_dict[person] = {'how_many_7': 1}  # first occurrence, at least one product
    else:
        people_dict[person]['how_many_7'] += 1
print(people_dict)

#5.5
print("5.5")
#how many different
cur.execute('SELECT e.FirstName, e.LastName, COUNT(DISTINCT p.ProductID) FROM Products p JOIN "Order Details" od ON p.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID JOIN Employees e ON o.EmployeeID = e.EmployeeID GROUP BY e.FirstName, e.LastName')
results = cur.fetchall()
for record in results:
    person = record[0] + ' ' + record[1]
    if person in people_dict.keys():
        people_dict[person]['how_many_different_products'] = record[2]
print(people_dict)
#which
for human in people_dict.keys():
    cur.execute('SELECT DISTINCT p.ProductName FROM Products p JOIN "Order Details" od ON p.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID JOIN Employees e ON o.EmployeeID = e.EmployeeID WHERE e.FirstName = "{name}" AND e.LastName = "{surname}"'.format(name=human.split()[0], surname=human.split()[1]))
    people_dict[human]['products_ordered'] = [product[0] for product in cur.fetchall()]
print(people_dict)

#5.6
print("5.6")
#filling product_list with all products ordered by any of those people
product_list = []
for human in people_dict.keys():
    for product in people_dict[human]['products_ordered']:
        if product not in product_list:
            product_list.append(product)
quantity_list = [0] * len(product_list)  #  a list carrying amounts of each product ordered
i = 0
for product in product_list:
    for human in people_dict.keys():
            cur.execute('SELECT od.Quantity FROM Products p JOIN "Order Details" od ON p.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID JOIN Employees e ON o.EmployeeID = e.EmployeeID WHERE e.FirstName = "{name}" AND e.LastName="{surname}" AND p.ProductName = "{product}"'.format(name=human.split()[0], surname=human.split()[1], product=product))
            result = cur.fetchone()
            if result is not None:
                quantity_list[i] += int(result[0])  # for each product we count how many items did each human do and aggregate the results in quantity_list
    i += 1

print(product_list[quantity_list.index(max(quantity_list))], quantity_list[quantity_list.index(max(quantity_list))])  # since we are interested in the most popular product

#5.7
print("5.7")

cur.execute('SELECT DISTINCT pr.ProductName, e.FirstName, e.LastName  FROM Products pr JOIN "Order Details" od ON pr.ProductID = od.ProductID JOIN Orders o ON od.OrderID = o.OrderID JOIN Employees e ON o.EmployeeID = e.EmployeeID')
results = cur.fetchall()
people_products = []

def in_people_products(person):
    """
    Check whether a certain person is already mentioned in the people_products list.
    :param person:
    :return:
    """
    for person_list in people_products:
        if person in person_list:
            return True
    return False

for result in results:
    person = result[1] + ' ' + result[2]
    if people_products == [] or in_people_products(person) == False:
        people_products.append([person, result[0]])  # e.g. ['John Smith', 'apple', 'banana', 'peach'...]
    else:
        for human in people_products:
            if human[0] == person:
                human.append(result[0])
similarity_ranking = []


def check_similarity(person_list):
    """
    The more products one has in common with ALFKI, the more similar his orderings are to him.
    :param person_list:
    :return:
    """
    products_in_common = 0
    for product in person_list:
        products_in_common += 1
    return products_in_common

for person in people_products:
     similarity_ranking.append([person[0], check_similarity(person[1:])])

similarity_ranking = sorted(similarity_ranking, key=lambda x: x[1], reverse=True)  # from the most similar towards least similar
for record in similarity_ranking:
    print(record[0], record[1])


