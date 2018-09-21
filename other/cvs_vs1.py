# -*- coding:utf-8*-
# -*- coding:utf-8*-
#coding=utf8
import sys

#python36

#功能  核对2个csv文件行数,如果相同不更新,如果行数不同   _py192这个文件会从 源文件最后数据添加, 没有运行前 确保2个cvs文件一样 可以用copy命令修复
#代码只是实现了功能,没有可读性


#from pandas import Series, DataFrame
#import pandas as pd
import numpy as np

import os
import os.path
#import time
#from datetime import datetime



#pd.set_option('display.width', 500)

# 输出磁盘
path_1 = "U:/ccex_to/"

# 策略名字
e_name = "d3/"


sy_list=[


"binance-BTCUSDT-1m_to_ok",

]

#filename1 = 'pmm_test2_1_2_duoying1_2_191_1k.csv'





for qihuo_name in sy_list:

    filename1 = path_1 + qihuo_name + '.csv'
    filename2 = path_1 + qihuo_name + '_py192.csv'


    #读取a1源文件, 统计列表数量


    try:
            with open(filename1) as f:
                lines = f.readlines() # 读取文本中所有内容，并保存在一个列表中，列表中每一个元素对应一行数据
		#print (lines) # 每一行数据都包含了换行符

    except IOError:

        continue


    else: print("111")



    print(len(lines))
    a1 = len(lines)

    #filename2 = 'O:\csv_to_mc\pmm_test2_1_2_duoying1_2_191_1kpy.csv'


    #读取b1源文件, 统计列表数量


    try:
        with open(filename2) as f:
            lines2 = f.readlines()
    #print (lines) # 每一行数据都包含了换行符

    except IOError:

        continue


    else: print("111")


    print(len(lines2))
    b1= len(lines2)

    #
    if a1>b1:


        with open(filename2,'a') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(lines[-(a1-b1)])
            #f.write("I am now studying in NJTECH.\n")


    #读取b1源文件, 统计列表数量
    with open(filename2) as f:
        lines2 = f.readlines()
    print (lines2[-1]) # 每一行数据都包含了换行符
    print (qihuo_name) # 每一行数据都包含了换行符

    #print ('------------')
    #for line in lines2:
    #    print (line.rstrip())
    #print ('------------')
