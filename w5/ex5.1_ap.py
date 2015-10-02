#!/usr/bin/python3
__author__ = 'aproxp'

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('northwind.db')
    con.text_factory = lambda x: str(x, 'latin1')
    cur = con.cursor()
    sql = "select products.productname, 'order details'.orderid from 'order details'" \
          "left join products on products.productid = 'order details'.productid " \
          "left join orders on 'order details'.orderid = orders.orderid " \
          "left join customers on customers.customerid = orders.customerid " \
          "where customers.customerid = 'ALFKI'"
    cur.execute(sql)
    all_data = cur.fetchall()

    print(all_data)

finally:
    if con:
        con.close()
