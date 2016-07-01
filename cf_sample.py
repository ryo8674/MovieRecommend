# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict

#Jaccard指数を計算
def jaccard(e1, e2):
    """
    :param e1: list of int
    :param e2: list of int
    :rtype: float
    """
    set_e1 = set(e1)
    set_e2 = set(e2)
    return float(len(set_e1 & set_e2)) / float(len(set_e1 | set_e2))

# 商品Xを購入した顧客IDが1,3,5ということ
product_x = [1, 3, 5]
product_a = [2, 4, 5]
product_b = [1, 2, 3]
product_c = [2, 3, 4, 7]
product_d = [3]
product_e = [4, 6, 7]

# 商品データ
products = {
    'A': product_a,
    'B': product_b,
    'C': product_c,
    'D': product_d,
    'E': product_e,
}

# # Xとの共起値を計算する
# print "共起"
# r = defaultdict(int)

# for key in products:
#     overlap = list(set(product_x) & set(products[key]))
#     r[key] = len(overlap)
# print r

# Xとのジャッカード指数を計算する
print "ジャッカード指数"
r2 = defaultdict(float)

for key in products:
    r2[key] = jaccard(product_x, products[key])
print r2

r2_max = max([(v,k) for k,v in r2.items()])[1]
#print "最大："+r2_max

src_set = set(product_x)
tag_set = set(products[r2_max])

matched_list =list (src_set & tag_set)
#print matched_list

matched_set = set(matched_list)
rec_list = list(tag_set - matched_set)
print "RecommendItem :"
print rec_list