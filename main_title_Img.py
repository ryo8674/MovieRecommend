# -*- coding: utf-8 -*-
# python 2.7.10


from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
from math import sqrt
from time import sleep
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

    #listを辞書化
    for k in range(0,len(user_list)):
        user_dict.setdefault(row[0],[]).append(user_list[k])

#ItemBaseFile(Image)
filenameusrImg = 'data/data_817/in_data_Img.csv'
usrImgfp = open(filenameusrImg,"rU")
usrImgreader = csv.reader(usrImgfp)
usrImg_dict = {}
usrImg_list = []

for row in usrImgreader:
    usrImg_list = row[1:]
    while usrImg_list.count("")>0:
        usrImg_list.remove("")
    usrImg_list = map(int,usrImg_list)

    #listを辞書化
    for k in range(0,len(usrImg_list)):
        usrImg_dict.setdefault(row[0],[]).append(usrImg_list[k])


#ItemBaseFile
filenameItem = 'data/data_817/in_data_Item_rate817.csv'
Userfp = open(filenameItem,"rU")
readerU = csv.reader(Userfp)

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
MovieDB_dict = {}
imageWeight = []
for row in readerMovie:
    MovieDB_dict[row[0]]=row[1].decode('utf-8')
    imageWeight.append(row[2])
imageWeight = map(float,imageWeight)


#transrate Movie to Image
filenametoImage ='data/Movie_toImage.csv'
toImagefp = open(filenametoImage,"rU")
readertoImage = csv.reader(toImagefp)
toImage_dict = {}
toImage_list = []
for row in readertoImage:
    toImage_list = row[1]
    # while toImage_list.count("")>0:
    #     toImage_list.remove("")
    toImage_list = map(int,toImage_list)
    for k in range(0,len(toImage_list)):
        toImage_dict.setdefault(row[0],[]).append(toImage_list[k])

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
# outfp = open('data/result/output_title_Img.csv', 'w')
outfp = open('data/result/output_title_Img2.csv', 'w')
csvWriter = csv.writer(outfp)

for usr in range(1,len(user_dict)+1):
    # 一時的に対象ユーザを格納する辞書
    tmp_dict ={}
    tmp_list =[]
    r_list = [] #類似度
    # count = 1
    tmp_dict = dict(user_dict)
    user_x = [] #対象ユーザ
    userImg_x = usrImg_dict[str(usr)] #対象ユーザの印象履歴
    user_x = user_dict[str(usr)]
    # user_dict.pop(str(usr))

    for i in range(1,len(user_dict)):
        if i == usr:
            continue
        if user_dict.has_key(str(i)):
            tmp_list = user_dict[str(i)]
        #ユーザXとの類似度計算
            r = jaccard(user_x, tmp_list)
            # r = cossim(user_x, user_list)
            r_list.append(r)

    while user_x.count("")>0:
        user_x.remove("")
    user_x = map(int,user_x)

    print "\nTargetUser：",usr,"\n"



    #--------------類似度最大価計算-------------
    ##・類似度と映画Noを取得
    ##・同値の場合の処理 => 映画Noを複数格納
    max =[]
    value = 0

    for i in range(0,len(r_list)):
    	if value < r_list[i]:
    		max=[]
    		max.insert(0,i+1)
    		value = r_list[i]
    	elif value == r_list[i]:
    		max.append(i+1)

    rate_list = []
    rate_dict = {}
    rate_list_Img = []
    rec_index = []
    rec_value = []

    re_rate_list = []
    re_rate_dict = {}
    re_rate_list_Img = []
    re_rec_index = []
    re_rec_value = []

    rec_list_bk = []
    rec_list =[]
    rec_list_Img = []
    # 類似度の高いユーザとそのユーザの視聴映画
    for i in range(0,len(max)):
        print "------------------------------------------------------------------------------------------------------------"
        # print "RecommendUser :",max[i],"\n"
        rec_user = user_dict[str(max[i])]

        src_set = set(user_x)
        tag_set = set(rec_user)

        matched_list =list (src_set & tag_set)
        #print matched_list

        matched_set = set(matched_list)

        #推薦候補リスト
        rec_list_bk = list(tag_set - matched_set)
        for i in rec_list_bk:
            rec_list.append(i)
        rec_list = list(set(rec_list))
        # print rec_list

        # #推薦候補リストに重みを付与
        # rate_list = []
        # rate_dict = {}
        #推薦候補順序付けリスト
        # rec_index = []
        # rec_value = []

        # # ##映画タイトルによる点数付け
        # for j in rec_list:
        #     rate = 0
        #     for k in user_x:
        #         rate_list=Itemrate_dict[str(k)]
        #         rate += rate_list[j-1]
        #     # print rate
        #     rate_dict[j] = rate

        ##タイトル+Imageによる点数付け
        for j in rec_list:
            tmp_j = toImage_dict[str(j)]
            rate = 0
            rate_Img = 0
            rate_tmp = 0
            for l in user_x:
                rate_list=Itemrate_dict[str(l)]
                rate += rate_list[j-1]
            for k in userImg_x:
                rate_list_Img = usrImg_dict[str(k)]
                # rate_Img += rate_list_Img[tmp_j[0]-1]
                rate_Img += rate_list_Img[tmp_j[0]-1] * imageWeight[tmp_j[0]-1]

            rate_dict[j] = rate + rate_Img

        #辞書を降順ソート
        for k, v in sorted(rate_dict.items(), key=lambda x:x[1] ,reverse = True):
            rec_index.append(k)
            rec_value.append(v)

        # 推薦候補が5作品未満の場合
        re_rec_list = []
        for i in range(1,136):
            re_rec_list.append(i)

        if len(rec_list) < 5:
            re_rec_list = list(set(re_rec_list)-src_set)
            re_rec_list = list(set(re_rec_list)-set(rec_list))

            for j in re_rec_list:
                tmp_j = toImage_dict[str(j)]
                rate = 0
                rate_Img = 0
                rate_tmp = 0
                for l in user_x:
                    re_rate_list=Itemrate_dict[str(l)]
                    rate += re_rate_list[j-1]
                for k in userImg_x:
                    re_rate_list_Img = usrImg_dict[str(k)]
                    # rate_Img += rate_list_Img[tmp_j[0]-1]
                    rate_Img += re_rate_list_Img[tmp_j[0]-1] * imageWeight[tmp_j[0]-1]

                re_rate_dict[j] = rate + rate_Img
        for k, v in sorted(re_rate_dict.items(), key=lambda x:x[1] ,reverse = True):
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
toImagefp.close()
usrImgfp.close()
