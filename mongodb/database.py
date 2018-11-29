#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:26:44 2018

@author: ece-student
"""

import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.test_database
collection = db.test_collection

def search_description(keyword):
    collection.create_index([('description', "text")])
    for i in collection.find({"$text": {"$search": keyword}}):
        print(i['username'])
        
def avg_pic_num():
    for i in collection.aggregate([{"$group":{"_id": "average", "num": {"$avg": "$picture num"}}}]):
        print(i['num'])

def max_descriptor():
    calculate = {}
    for i in collection.find():
#        print(i)
        for des in i['count']:
            calculate.setdefault(des, 0)
            if des in calculate:
                calculate[des] = calculate[des] + i['count'][des]
#    print(calculate)
    descriptor = max(calculate, key=calculate.get)
    print(descriptor)

if __name__ == '__main__':
    print('the average picture number of the system right now is:')
    avg_pic_num()
    print('the most popular descriptor of the system is:')
    max_descriptor()
    keyword = input('please enter the description here:')
    print('here are the users who have this description:')
    search_description(keyword)