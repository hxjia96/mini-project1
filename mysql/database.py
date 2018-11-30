#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:26:44 2018

@author: ece-student
"""

import pymysql

db = pymysql.connect("localhost","root","123456","miniproject3") 
cursor = db.cursor()

def search_description(keyword):
    db = pymysql.connect("localhost","root","123456","miniproject3") 
    cursor = db.cursor()
    sql = "SELECT USERNAME FROM information1 WHERE LOCATE('"+keyword+"', DESCRIPTION) > 0"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        print(i[0])
    db.close()
        
def avg_pic_num():
    db = pymysql.connect("localhost","root","123456","miniproject3") 
    cursor = db.cursor()
    sql = "SELECT AVG(PICTURE_NUM) FROM information1"
    cursor.execute(sql)
    result = cursor.fetchall()
#    for i in result:
    print(result[0][0])
    db.close()

def max_descriptor():
    calculate = {}
    db = pymysql.connect("localhost","root","123456","miniproject3") 
    cursor = db.cursor()
    sql1 = "SELECT DESCRIPTION FROM information1"
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    sql2 = "SELECT COUNT FROM information1"
    cursor.execute(sql2)
    result2 = cursor.fetchall()    
    for i in range(0, len(result1)):
        description = result1[i][0].split(',')
#        print(len(description))
        count = result2[i][0].split(',')
#        print(len(count))
        for n in range(0, len(description)):
            calculate.setdefault(description[n], 0)
            calculate[description[n]] = calculate[description[n]] + int(count[n])
    descriptor = max(calculate, key=calculate.get)
    print(descriptor)
    db.close()


if __name__ == '__main__':
    print('the average picture number of the system right now is:')
    avg_pic_num()
    print('the most popular descriptor of the system is:')
    max_descriptor()
    keyword = input('please enter the description here:')
    print('here are the users who have this description:')
    search_description('fan')