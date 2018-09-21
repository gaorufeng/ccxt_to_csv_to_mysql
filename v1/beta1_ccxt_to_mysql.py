# _*_ coding:utf-8 _*_
#python27


#新建表,符合 ccxt1

# beta1_ccxt_to_mysql 负责新建表,和字段, beta2_ccxt_to_mysql负责导入csv ; beta1and2_ccxt_to_mysql 是2个一起运行

#20180901 肯定还能修改,先实现功能


#from sqlalchemy import create_engine
import MySQLdb
import os
#import pandas as pd

#import tushare as ts

#from pandas import Series, DataFrame

#import numpy as np


#from datetime import datetime
#from datetime import *
#import time

#pd.set_option('display.width', 200)



##需要修改的地方

conn = MySQLdb.connect(host='192.168.100.151', user='root', passwd='xxxxxxx', charset="utf8")

#数据库名
data_name = 'ccxt1'

#获取目录下面csv的文件名 导入到列表
file_path = 'Y://vps1/'

##修改结束





codenameall = []
for root, dirs, files in os.walk(file_path):# 注意：这里请填写数据文件在您电脑中的路径
    if files:
        for f in files:
            if '.csv' in f:
                codenameall.append(f.split('.csv')[0])
print (codenameall)

# 股票代码
#codenameall = ['sh600000_noid']

# 循环导入上述股票

for cdname in codenameall:

    acdname1 = cdname

    cursor = conn.cursor()

    #数据库名字
    conn.select_db(data_name)

    #Timestamp,Open,High,Low,Close,Volume

    
    #数据结构应该可以更好,这里就全部写成 double 了
    try:
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS `%s`(
              `Timestamp` double NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
              `Open` double DEFAULT NULL,
              `High` double DEFAULT NULL,
              `Low` double DEFAULT NULL,
              `Close` double DEFAULT NULL,
              `Volume` double DEFAULT NULL

          ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
          """ % acdname1)


        cursor.close()
        print "sql ok"
    except:
        cursor.close()
        print "sql not ok, already exists"

