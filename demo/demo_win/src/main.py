#! /usr/local/bin/python
# -*- coding: utf-8 -*-
# python 2.7.9


from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import fileoperation as fo
import itemrate as ir
import getInput as gi
import titletoimg as tti

#jaccard係数
def jaccard(e1, e2):
    """
    :param e1: list of int
    :param e2: list of int
    :rtype: float
    """
    set_e1 = set(e1)
    set_e2 = set(e2)
    return float(len(set_e1 & set_e2)) / float(len(set_e1 | set_e2))


def recommend():
    output = 'data/result/output.csv'
    result = []

    #映画知識ベース
    imageWeight = []
    MovieDB_dict = {}
    MovieDB_filename = 'data/MovieKB.csv'
    fo.fileRead(MovieDB_filename,imageWeight,MovieDB_dict,num_type = float,flag = 1)

    #映画評価データ
    Eval_list = []
    Eval_dict = {}
    filename = 'data/raw_data_817.csv'
    fo.fileRead(filename,Eval_list,Eval_dict,num_type = int,flag = 0)
    gi.getInput(filename,'data/in_data_817.csv',135,1)
    gi.getInput(filename,'data/in_data2.csv',135,2)

    tti.titletoImg()
    filename = 'data/in_data_Img.csv'
    gi.getInput(filename,'data/in_data3.csv',176,3)

    ir.itemrate()

    output = 'data/result/output.csv'
    result = []

    #視聴履歴の獲得
    user_list =[]
    user_dict = {}
    filename = 'data/in_data_817.csv'
    fo.fileRead(filename,user_list,user_dict,num_type = int,flag = 0)

    #視聴した印象
    usrImg_list = []
    usrImg_dict = {}
    filename = 'data/in_data_Img.csv'
    fo.fileRead(filename,usrImg_list,usrImg_dict,num_type = int,flag = 0)

    #映画のタイトルの類似度
    Itemrate_list = []
    Itemrate_dict = {}
    filename = 'data/in_Item_rate.csv'
    fo.fileRead(filename,Itemrate_list,Itemrate_dict,num_type = float,flag = 3)

    #印象の類似度
    ImgItem_list = []
    ImgItem_dict = {}
    filename = 'data/in_Img_rate.csv'
    fo.fileRead(filename,ImgItem_list,ImgItem_dict,num_type = float,flag = 3)

    #映画のタイトルを印象に変換
    toImage_list = []
    toImage_dict = {}
    filename ='data/Movie_toImage.csv'
    fo.fileRead(filename,toImage_list,toImage_dict,num_type = int,flag = 2)

    for usr in range(1,len(user_dict)+1):
        tmp_dict ={}
        tmp_list =[]
        r_list = [] #類似度
        tmp_dict = dict(user_dict)
        user_x = [] #対象ユーザ
        userImg_x = usrImg_dict[str(usr)]   #対象ユーザの印象履歴
        user_x = user_dict[str(usr)]

        #各ユーザと類似度計算
        for i in range(1,len(user_dict)):
            if i == usr:
                continue
            if user_dict.has_key(str(i)):
                tmp_list = user_dict[str(i)]
                r = jaccard(user_x, tmp_list)
                r_list.append(r)

        while user_x.count("")>0:
            user_x.remove("")
        user_x = map(int,user_x)

        print "\nTargetUser：",usr,"\n"

        max =[]
        value = 0
        #最も高い類似度のユーザを決定
        for i in range(0,len(r_list)):
        	if value < r_list[i]:
        		max=[]
        		max.insert(0,i+1)
        		value = r_list[i]
        	# elif value == r_list[i]:
        	# 	max.append(i+1)

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
            print "----------------------------------------------------------------------------------------"
            print "RecommendUser :",max[i]
            print "----------------------------------------------------------------------------------------"

            rec_user = user_dict[str(max[i])]

            src_set = set(user_x)
            tag_set = set(rec_user)

            matched_list =list (src_set & tag_set)
            matched_set = set(matched_list)

            #推薦候補リスト
            rec_list_bk = list(tag_set - matched_set)
            for i in rec_list_bk:
                rec_list.append(i)
            rec_list = list(set(rec_list))

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
                    rate_list_Img = ImgItem_dict[str(k)]
                    # rate_Img += rate_list_Img[tmp_j[0]-1]
                    rate_Img += rate_list_Img[tmp_j[0]-1]

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
                        re_rate_list_Img = ImgItem_dict[str(k)]
                        # rate_Img += rate_list_Img[tmp_j[0]-1]
                        rate_Img += re_rate_list_Img[tmp_j[0]-1]

                    re_rate_dict[j] = rate + rate_Img
            for k, v in sorted(re_rate_dict.items(), key=lambda x:x[1] ,reverse = True):
                rec_index.append(k)
                rec_value.append(v)


        #出力ファイル書き込み
        print "RecommendItem :"

        for w in rec_index[0:5]:
            outlist = []
            outlist.append(usr)
            outlist.append(w)
            print w,MovieDB_dict[str(w)]
            tmp_user=[]
            tmp_user = Eval_dict[str(usr)]

            outlist.append(tmp_user[w-1])
            result.append(outlist)

        print "----------------------------------------------------------------------------------------"
    fo.fileWrite(output,result,2)

if __name__ == "__main__":
    recommend()
