# -*- coding:utf-8 -*-
#py36

# 备份 151 mysql  ccxt1

#备份mysql 到csv


import pandas as pd
import pymysql
import os
import sys
from sqlalchemy import create_engine


conn = pymysql.connect(host='127.0.0.1', \
               user='root',password='xxxxxxx', \
               db='ccxt1',charset='utf8', \
               use_unicode=True)

file_path = 'O:/vps1/'
#获取需要备份的表名字,这里是下载下来的csv路径

codenameall = []
for root, dirs, files in os.walk(file_path):# 注意：这里请填写数据文件在您电脑中的路径
    if files:
        for f in files:
            if '.csv' in f:
                codenameall.append(f.split('.csv')[0])
print (codenameall)

#table_name_1 = "binance-BTCUSDT-1m"

for cdname in codenameall:


    table_name_1 = cdname

    table_name = "`" + table_name_1 + "`"

    sql = 'select * from ' + table_name
    df = pd.read_sql(sql, con=conn)


    #选择保存
    df.to_csv('D:/backup_mysql/' +table_name_1+'.csv',index=False)
    
    
#使用tushare的pandas进行to_sql操作时的No module named 'MySQLdb'错误处理  

#https://www.cnblogs.com/magicc/p/6490671.html

#python3.*报“ImportError: No module named ‘MySQLdb'” 
#https://www.cnblogs.com/TaleG/p/6735099.html
