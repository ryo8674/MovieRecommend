#! /usr/local/bin/python
# -*- coding: utf-8 -*-
# python 2.7.9

from math import sqrt
import fileoperation as fo

def totalList(listname):
    sum = 0
    for l in listname:
        sum += l
    return sum

def getColumn(listname,index):
    res = []
    for l in listname:
        res.append(l[index])
    return res

def collocation(list1,list2):
    count = 0
    for i in range(len(list1)):
        if list1[i] == 1 and list2[i] == 1:
            count += 1
    return count

def collocation2(i,listname,n):
    count = 0
    for j in range(n):
        if i == j:
            continue
        else:
            cl_i = getColumn(listname,i)
            cl_j = getColumn(listname,j)
            c = collocation(cl_i,cl_j)
        count += c
    return count


def compute_item_similarities(listname,n):
    sims = []

    for i in range(n):
        l1=[]
        l1.append(i+1)
        tmp = collocation2(i,listname,n)

        for j in range(n):
            if j == i:
                sim = 1.0
            elif tmp == 0.0:
                sim = 0.0
            else:
                cl_i = getColumn(listname,i)
                cl_j = getColumn(listname,j)
                # ri は アイテム i に関する全ユーザの評価を並べた列ベクトル
                sim = float(collocation(cl_i,cl_j)) / float(tmp)

            l1.append(sim)
        sims.append(l1)
    return sims

def getRate(in_filename,out_filename,n):
    tmp_list = []
    for i in range(n+1):
        tmp_list.append(i)

    user_list =[]
    fo.fileRead(in_filename,user_list,0,num_type = int,flag = 5)

    sims = compute_item_similarities(user_list,n)
    sims.insert(0,tmp_list)
    fo.fileWrite(out_filename,sims,2)

def itemrate():
    in_file1 = 'data/in_data2.csv'
    in_file2 = 'data/in_data3.csv'
    out_file1 = 'data/in_Item_rate817.csv'
    out_file2 = 'data/in_Img_rate817.csv'

    getRate(in_file1,out_file1,135)
    getRate(in_file2,out_file2,176)


if __name__ == "__main__":
    main()
