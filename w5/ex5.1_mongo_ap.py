__author__ = 'aproxp'

from pymongo import MongoClient

client = MongoClient()

db = client['Northwind']

collection = db['products']

print(collection)

collection.