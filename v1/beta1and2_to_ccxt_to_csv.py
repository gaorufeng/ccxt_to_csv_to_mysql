# _*_ coding:utf-8 _*_
#python27


#新建表,符合 ccxt1

#20180901 肯定还能修改,先实现功能

#from sqlalchemy import create_engine
import MySQLdb
import os
import csv




##需要修改的地方
#engine = create_engine('mysql://root:密码@192.168.100.151/stock?charset=utf8')
conn = MySQLdb.connect(host='192.168.100.151', user='root', passwd='xxxxxxx', charset="utf8")
db = MySQLdb.connect(host='192.168.100.151',user='root', passwd='xxxxxxxx', charset="utf8")


#数据库名
data_name = 'ccxt1'

#获取目录下面csv的文件名 导入到列表
file_path = 'Y://vps1/'

##修改结束

#连接数据库（参照MySQL Workbench中的设定）


data_name2 = 'USE ccxt1'
#数据库名 只修改 ccxt1 , 保留USE



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






cur = db.cursor()


#print (codenameall)

for cdname in codenameall:

    table_name = cdname

    filename = file_path + cdname + '.csv'

    Generaldata = csv.reader(file(filename))

    cur.execute(data_name2)
    # cur.execute('DROP TABLE IF EXISTS T1') #用于卸掉旧表


    #for row in Generaldata:
    #Generaldata 第一行有导入

    for row in list(Generaldata)[1:]:
    ##(Generaldata)[1:] 去除第一行
        cur.execute('''INSERT ignore INTO `%s` (Timestamp,Open,High,Low,Close,Volume) VALUES(%s,%s,%s,%s,%s,%s)''' % (table_name,row[0],row[1],row[2],row[3],row[4],row[5]))
        #这里使用INSERT ignore INTO ,不会重复,也不会覆盖, 详见 底下备注1
    db.commit()




#备注 1
#INSERT ignore INTO
# MySQL避免插入重复记录的方法  https://www.cnblogs.com/prayer21/p/6018864.html
#mysql 忽略主键冲突、避免重复插入的几种方式  https://my.oschina.net/leejun2005/blog/150510
#MySQL批量插入遇上唯一索引避免方法（避免导入重复数据）  https://blog.csdn.net/jinmaodao116/article/details/54134480

#本文参考
#用python将CSV转入Mysql  https://wwshen.gitbooks.io/omooc2py/content/0MOOC/CSVtoMYSQL.html
