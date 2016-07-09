# -*- coding: utf-8 -*-
## 環境:Python 2.7.10

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
from math import sqrt
import csv

__author__ = 'Ryo Yamada'

#----------------類似度--------------------
#jaccard指数
def jaccard(e1, e2):
    """
    :param e1: list of int
    :param e2: list of int
    :rtype: float
    """
    set_e1 = set(e1)
    set_e2 = set(e2)
    return float(len(set_e1 & set_e2)) / float(len(set_e1 | set_e2))

#Cosine類似度
def cossim(e1,e2):
    """
    :param e1: list of int
    :param e2: list of int
    :rtype: float
    """
    set_e1 = set(e1)
    set_e2 = set(e2)
    return float(len(set_e1 & set_e2)) / (sqrt(float(len(set_e1)))*sqrt(float(len(set_e2))))


#推薦対象ユーザ情報
#ReadFile
filename = 'data/data_817/in_data_817.csv'
fp = open(filename,"rU")
reader = csv.reader(fp)
# header = next(reader)
user_dict = {}
user_list = []

for row in reader:
    user_list = row[1:]
    while user_list.count("")>0:
        user_list.remove("")
    user_list = map(int,user_list)

    # #ユーザXとの類似度計算
    # r = jaccard(user_x, user_list)
    # # r = cossim(user_x, user_list)
    # r_list.append(r)

    #listを辞書化
    for k in range(0,len(user_list)):
        user_dict.setdefault(row[0],[]).append(user_list[k])

#ItemBaseFile
filenameItem = 'data/data_817/in_data_Item_rate817.csv'
Userfp = open(filenameItem,"rU")
readerU = csv.reader(Userfp)

#ItemBaseFile
Itemrate_list = []
Itemrate_dict = {}
headerU = next(readerU)

for row in readerU:
    Itemrate_list = row[1:]
    while Itemrate_list.count("")>0:
            Itemrate_list.remove("")
    Itemrate_list = map(float,Itemrate_list)
    for k in range(0,len(Itemrate_list)):
        Itemrate_dict.setdefault(row[0],[]).append(Itemrate_list[k])

#MovieDataBase ->dictionary
filenameMovie = 'data/MovieDB.csv'
Moviefp = open(filenameMovie,"rU")
readerMovie = csv.reader(Moviefp)
MovieDB_dict={}
for row in readerMovie:
    MovieDB_dict[row[0]]=row[1].decode('utf-8')

#映画評価データ
filenameEval = 'data/data_817/raw_data_817.csv'
Evalfp = open(filenameEval,"rU")
readerEval = csv.reader(Evalfp)
Eval_dict ={}
Eval_list = []
for row in readerEval:
    Eval_list = row[1:]
    while Eval_list.count("")>0:
        Eval_list.remove("")
    Eval_list = map(int,Eval_list)
    for k in range(0,len(Eval_list)):
        Eval_dict.setdefault(row[0],[]).append(Eval_list[k])

#対象ユーザ情報
#推薦対象ユーザをランダムに取得 -> 視聴履歴DBは対象ユーザ以外を取得

#出力ファイル生成
outfp = open('data/result/outputI.csv', 'w')
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

    while user_x.count("")>0:
        user_x.remove("")
    user_x = map(int,user_x)

    print "\nTargetUser：",usr,"\n"

    rate_list = []
    rate_dict = {}
    rec_index = []
    rec_value = []
    rec_list_bk = []
    rec_list =[]
    print "------------------------------------------------------------------------------------------------------------"

    for j in range(1,len(MovieDB_dict)+1):
        rate = 0
        for k in user_x:
            rate_list=Itemrate_dict[str(k)]
            rate += rate_list[j-1]
        # print rate
        rate_dict[j] = rate
    # print rate_dict
    for k in user_x:
        rate_dict.pop(k)

    #辞書を降順ソート
    for k, v in sorted(rate_dict.items(), key=lambda x:x[1] ,reverse = True):
        rec_index.append(k)
        rec_value.append(v)

    # #昇順ソート
    # rec_list.sort()

    #出力ファイル書き込み
    print "RecommendItem :"
        # v = 0
    for w in rec_index[0:5]:
        outlist = []
        outlist.append(usr)
        outlist.append(w)
        # outlist.append(rec_value[v])
        # v += 1
        print w,MovieDB_dict[str(w)]
        tmp_user=[]
        tmp_user = Eval_dict[str(usr)]
        # print tmp_user[w-1]
        outlist.append(tmp_user[w-1])
        csvWriter.writerow(outlist)

    # # print "RecommendItem :",rec_index[0:5]
    # print "RecommendItem :",rec_list

    print "------------------------------------------------------------------------------------------------------------"
    # user_dict =dict(tmp_dict)

fp.close()
Userfp.close()
Moviefp.close()
Evalfp.close()
outfp.close()
