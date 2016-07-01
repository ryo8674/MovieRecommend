# -*- coding: utf-8 -*-
## 環境:Python 2.7.9

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
from math import sqrt
import csv


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
filename = 'in_data.csv'
fp = open(filename,"rU")
reader = csv.reader(fp)
header = next(reader)

#対象ユーザ情報
# user_x = [2, 3, 4, 5, 6, 7, 8, 120, 121, 130, 135]
user_x = header[1:]


user_dict={}
user_list=[]
rec_dict={}
r_list = []

for row in reader:
    user_list = row[1:]
    while user_list.count("")>0:
        user_list.remove("")
    user_list = map(int,user_list)

    #ユーザXとの類似度計算
    r = jaccard(user_x, user_list)
    # r = cossim(user_x, user_list)
    r_list.append(r)

    #listを辞書化
    for k in range(0,len(user_list)):
        user_dict.setdefault(row[0],[]).append(user_list[k])

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

# 類似度の高いユーザとそのユーザの視聴映画
for i in range(0,len(max)):
    print "------------------------------------------------------------------------------------------------------------"
    print "RecommendUser :",max[i],"\n"
    rec_user = user_dict[str(max[i])]

    src_set = set(user_x)
    tag_set = set(rec_user)

    matched_list =list (src_set & tag_set)
    #print matched_list

    matched_set = set(matched_list)
    rec_list = list(tag_set - matched_set)
    rec_list.sort()
    print "RecommendItem :",rec_list
print "------------------------------------------------------------------------------------------------------------"

fp.close()
