# -*- coding: utf-8 -*-
## 環境:Python 2.7.10

##映画視聴履歴を印象に変換

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
from math import sqrt
import csv

#ファイル読み込み
def fileRead(filename,listname,dict_name,num_type,flag):
    fp = open(filename,"rU")
    reader = csv.reader(fp)

    for row in reader:
        if flag == 1:
            dict_name[row[0]]=row[1]
            # listname.append(row[2])
            # listname = map(num_type,listname)
        else:
            if flag == 2:
                listname = row[1]
            else:
                listname = row[1:]
                while listname.count("")>0:
                    listname.remove("")
            listname = map(num_type,listname)
            #listを辞書化
            for k in range(0,len(listname)):
                dict_name.setdefault(row[0],[]).append(listname[k])

if __name__ == "__main__":

    #視聴履歴獲得
    user_dict = {}
    user_list = []
    filename = 'data/in_data_817.csv'
    csvRead(filename,user_list,user_dict,num_type = int,flag = 0)

    #映画知識ベース
    MovieDB_dict={}
    MovieDB_list=[]
    filename = 'data/MovieDB.csv'
    csvRead(filename,MovieDB_list,MovieDB_dict,num_type = int,flag = 1)

    #映画評価データ
    Eval_list = []
    Eval_dict = {}
    filename = 'data/raw_data_817.csv'
    fileRead(filename,Eval_list,Eval_dict,num_type = int,flag = 0)

    #映画のタイトルを印象に変換
    toImage_list = []
    toImage_dict = {}
    filename ='data/Movie_toImage.csv'
    fileRead(filename,toImage_list,toImage_dict,num_type = int,flag = 2)

    #出力ファイル生成
    outfp = open('data/in_data_Img.csv', 'w')
    csvWriter = csv.writer(outfp)

    for usr in range(1,len(user_dict)+1):
        # 一時的に対象ユーザを格納する辞書
        tmp_dict ={}
        tmp_list =[]
        r_list = [] #類似度
        # count = 1
        tmp_dict = dict(user_dict)
        user_x = [] #対象ユーザ
        user_x = user_dict[str(usr)]
        # user_dict.pop(str(usr))
        Image_list=[]
        for i in user_x:
            Image_list.append(ImageDB_dict[i])
        out_list=[]
        out_list = list(set(Image_list))
        out_list.sort()
        csvWriter.writerow(out_list)
