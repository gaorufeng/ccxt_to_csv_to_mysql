
# -*- coding:utf-8*-
# -*- coding:utf-8*-

#ccex 数据时间戳是unix,转换成 date和time时间,数据来源以及导入mysql,这里是从mysql获取
#代码只是实现了功能,没有可读性
#python36

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

import os
import os.path
import time


import time
from datetime import datetime

from datetime import timedelta


import pandas as pd
import pymysql
import sys
from sqlalchemy import create_engine


conn = pymysql.connect(host='127.0.0.1', \
               user='root',password='xxxxxx', \
               db='ccxt1',charset='utf8', \
               use_unicode=True)



table_name_1 = "binance-BTCUSDT-1m"



table_name = "`" + table_name_1 + "`"

sql = 'select * from ' + table_name
df = pd.read_sql(sql, con=conn)



df.sort_values('Timestamp', inplace=True)

#print(df)


#unix时间转换
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')


# 重点 把 date列 字符串 转换成日期格式

df['Timestamp'] = pd.to_datetime(df['Timestamp'])



#时区处理#
df['Timestamp']=df['Timestamp']+timedelta(hours=8)
#主要是binance 和 北京时间相差8小时,其他交易所根据情况更改


#下面如果 你需要的是 date和time连载一起的就跳过 ----

#提取time时间
df['time'] = pd.to_datetime(df['Timestamp'],format='%H%M')
df['time'] = pd.to_datetime(df['time']).dt.time

#提取date时间
#df['date'] = pd.to_datetime(df['date'],format='%H%M')
df['date'] = pd.to_datetime(df['Timestamp']).dt.date



#插入time
mid = df['time']
df.drop(labels=['time'], axis=1,inplace = True)
df.insert(1, 'time', mid)


#插入date,解决列的前后位置 使得 date最前面,其次是time
mid = df['date']
df.drop(labels=['date'], axis=1,inplace = True)
df.insert(1, 'date', mid)
del df['Timestamp']

# ------你需要的是 date和time连载一起的上面可跳过 只需要把 ['Timestamp'] 改成 ['datetime'],方法参考 date和time位置处理-----







qihuo_name = 'binance_BTCUSDT'

zhouqi = '1m_ok'

print(df[-10:])


try:
    df.to_csv('o:/ccex_to_/' + table_name_1 +"_to_ok.csv", index=False)

except Exception:
    print(qihuo_name + u'出错')
else:
    print(qihuo_name+ u'输出ok')


#备注 碰到的错误

#使用tushare的pandas进行to_sql操作时的No module named 'MySQLdb'错误处理 

#https://www.cnblogs.com/magicc/p/6490671.html

#python3.*报“ImportError: No module named ‘MySQLdb'” 
#https://www.cnblogs.com/TaleG/p/6735099.html

#Python中pandas函数操作数据库

#https://blog.csdn.net/u011301133/article/details/52488690

