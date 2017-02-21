#! /usr/local/bin/python
# -*- coding:utf-8 -*-

import csv
import fileoperation as fo

def getInput(in_filename,out_filename,n,flag):
    flag += 5
    if flag == 6:
        n += 1

    in_list = [[0]* (n+1)]*817
    out_list = [[0 for i in range(n)] for j in range(817)]

    fo.fileRead(in_filename,in_list,0,num_type = 0,flag = flag)

    if flag == 6 or flag == 7:
        k = 0
        if flag == 6:
            k = 1

        for i in range(817):
            for j in range(k,n):
                if in_list[i][j] == '1' or in_list[i][j] == '2':
                    if flag == 6:
                        in_list[i][j] = str(j)
                    else:
                        in_list[i][j] = 1
                else:
                    if flag == 6:
                        in_list[i][j] = ""
                    else:
                        in_list[i][j] = 0

        fo.fileWrite(out_filename,in_list,2)

    else:
        for i in range(len(in_list)):
            for j in in_list[i]:
                out_list[i][j-1] = 1
        fo.fileWrite(out_filename,out_list,2)


# if __name__ == "__main__":
    # in_filename = "data/raw_data_817.csv"
    # out_filename = "data/in_data_817.csv"

    # in_filename = "data/raw_data_817.csv"
    # out_filename = "data/in_data2.csv"

    # in_filename = "data/in_data_Img.csv"
    # out_filename = "data/in_data3.csv"

    # getInput(in_filename,out_filename,135,6)
    # getInput(in_filename,out_filename,135,7)
    # getInput(in_filename,out_filename,176,8)
