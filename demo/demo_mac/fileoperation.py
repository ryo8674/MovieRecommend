#! /usr/local/bin/python
# -*- coding: utf-8 -*-
# python 2.7.9
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import csv

def fileRead(filename,listname,dict_name,num_type,flag):
    fp = open(filename,"rU")
    reader = csv.reader(fp)
    i = 0
    if flag == 3:
        header = next(reader)

    for row in reader:
        if flag == 1:
            dict_name[row[0]]=row[1]
            # listname.append(row[2])
            # listname = map(num_type,listname)
        elif flag == 6 or flag == 7 or flag == 8:
            if flag == 6:
                listname[i] = row
            else:
                listname[i] = row[1:]
                if flag == 8:
                    while listname[i].count("")>0:
                        listname[i][int(listname[i.index("")])]=0
                    listname[i] = map(int,listname[i])
            i += 1
        elif flag == 5:
            listname.append(map(num_type,row))
        else:
            if flag == 2:
                listname = row[1]
            elif flag == 4:
                listname = row
            else:
                listname = row[1:]
                while listname.count("")>0:
                    listname.remove("")
            listname = map(num_type,listname)
            #listを辞書化
            for k in range(0,len(listname)):
                dict_name.setdefault(row[0],[]).append(listname[k])

def fileWrite(filename,listname,div):
    fp = open(filename, 'w')
    csvWriter = csv.writer(fp)
    if div == 1:
        csvWriter.writerow(listname)
    else:
        csvWriter.writerows(listname)
