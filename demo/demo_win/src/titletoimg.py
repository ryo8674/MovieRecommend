# -*- coding: utf-8 -*-
## 環境:Python 2.7.10

##映画視聴履歴を印象に変換

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
from math import sqrt
import csv
import fileoperation as fo

def titletoImg():
    #視聴履歴獲得
    user_dict = {}
    user_list = []
    filename = 'data/in_data_817.csv'
    fo.fileRead(filename,user_list,user_dict,num_type = int,flag = 0)

    #映画知識ベース
    MovieDB_dict={}
    MovieDB_list=[]
    filename = 'data/MovieKB.csv'
    fo.fileRead(filename,MovieDB_list,MovieDB_dict,num_type = int,flag = 1)

    #映画のタイトルを印象に変換
    toImage_list = []
    toImage_dict = {}
    filename ='data/Movie_toImage.csv'
    fo.fileRead(filename,toImage_list,toImage_dict,num_type = int,flag = 1)

    out_list=[]
    output = 'data/in_data_Img.csv'

    for usr in range(1,len(user_dict)+1):
        user_x = user_dict[str(usr)]
        Image_list=[]
        for i in user_x:
            Image_list.append(toImage_dict[str(i)])

        Image_list = list(set(Image_list))
        Image_list.sort()
        Image_list.insert(0,str(usr))
        out_list.append(Image_list)
    fo.fileWrite(output,out_list,2)


if __name__ == "__main__":
    titletoImg()
