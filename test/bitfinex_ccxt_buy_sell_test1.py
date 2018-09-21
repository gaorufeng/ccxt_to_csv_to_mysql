# _*_ coding:utf-8 _*_

#!!!!!!!!!!!!!!!!!
#!!!注意 jion文件内 切换到 多头平仓和空头平仓时候要小心, 因为这个是以市价来执行的
#!!!!!!!!!!!!!!!!

'''
#python36 at pycharm调试
# 源代码修改来自  数字货币量化投资入门课程  https://study.163.com/course/courseMain.htm?courseId=1005149010
#20180919 目前仅仅是内测,有太多没有考虑的bug存在, 没搞懂前请不要实盘
#如果你非要运行,先查看 目前eos的价格

同时设置 价格, 如果当前eos/usd 是5元
pirce =3
#买多价格
pirce_kong = 7
#卖空价格
当信号符合时系统会发出委托买单3usd  空单7, 你只需即使撤销不会马上成交


!!!!!!!!!!!!!!!!!
#!!!注意 jion文件内 切换到 多头平仓和空头平仓时候要小心, 因为这个是一市价来执行的
!!!!!!!!!!!!!!!!


#程序仅仅为交易模块,不包含信号, 你可以在程序运行的时候 手动修改 txt_in_001.json文件内的
# "mp_latest":0,
# "mp_old":0, 参数
#默认是空仓

#已知bug
# 2018 09 18 对于策略开启时,正好的建仓时候,实盘如果已经有仓位了,但是 此程序可能会再次开
#对于一些访问bitf的函数没有做错误处理, 可能网络出现问题或者无法拿到数据会程序中断
#出错以后跳转到哪里? 重新尝试还是?
#如何处理持仓小尾巴0.014580.01451
#为了避免小尾巴可以把小于0.5的仓位转移到融资里面
# 需要在策略中实现资金管理策略  比如当卖空前和开多单前 检查资产和持仓的对比,超过一定比例拒绝开仓.
'''


import ccxt
import pandas as pd
import json
from time import sleep
import datetime


pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

mp_local = 0



#开仓品种
symbol = 'EOS/USDT'
#开仓价格

pirce =3
#买多价格

pirce_kong = 7
#卖空价格

#开仓 数量
kaichang_shuliang = 4
#开仓精度 (用于识别 不同策略同一个品种 的在线委托单和持仓情况)
chelue_jindu = 0.01
#每个策略设置不同的进度 (注意原有仓位小尾巴对进度的影响)
#考虑到 查看当前订单(未成交)是以委托编号 查询open 状态,如果委托编号意外丢失,
# 此时可以识别精度来判断委托单是否已经在订单列表,避免重复开仓. 仅对为成交的委托单有效,对已经成交的无效



#开仓总数量,包含精度
kaichang_zhongshu = kaichang_shuliang + chelue_jindu


weituo_bianhao = 0


#委托编号
weituo_zhuangtai = ""

# =====创建bitfinex交易所
bitfinex = ccxt.bitfinex()
# df = bitfinex.fetch_ohlcv("BTC/USDT", "15m")
# print(df)

bitfinex.apiKey = 'xxxx'
bitfinex.secret = 'xxxxx'


# 仓位检查
def changwei_jiancha():


    # =====获取bitfinex账户资产
    try:
        balance_exchange = bitfinex.fetch_balance()  # 获取exchange账户资产
        print("获取exchange账户资产正常")
    except:
        print("获取exchange账户资产出错,下面将会出错")


    print(balance_exchange['free']['EOS'])
    changwei = balance_exchange['free']['EOS']

    #返回 eos可用数量

    return changwei

    # 仓位检查

def changwei_jiancha_margin():
    # =====获取bitfinex账户资产 _margin
    balance_margin = bitfinex.fetch_balance({'type': 'trading'})
    print(balance_margin['free']['EOS'])
    changwei_margin = balance_margin['free']['EOS']
    print(changwei_margin)
    # 返回 eos可用数量

    return changwei_margin


        #委托单查询

def weituo_changxun():
    balance_exchange = bitfinex.fetch_balance()  # 获取exchange账户资产
    print("委托查询")

def weituo_changxun_kong():
    balance_margin = bitfinex.fetch_balance({'type': 'trading'})  # 获取margin账户资产
    print("委托查询")

def open_orders():
    # # 返回尚未成交的订单
    a = 0
    dingdan_amount = []
    try:
        order_info = bitfinex.fetch_open_orders(symbol='EOS/USDT', limit=20)  # limit参数控制返回最近的几条
        print("获取订单信息正常")

        if len(order_info):
            print("现在有在线委托单")
            #下面使用for是为了查看多个委托单

            #声明一个 数组 ,里面包含了现在委托品种的 委托数量

            for i in order_info:

                print("在线 委托数量")
                print(i['amount'])
                print(kaichang_zhongshu)
                if i['amount'] == kaichang_zhongshu:
                    a = 999

                #如果在线委托单 = 开仓总数, 说明委托单已经提交,未成交状态
                else:
                    # 如果委托单 不等于  开仓总数,说明此策略没有发出委托/或已经成交
                    temp = 0
        else:
            print("现在没有委托单")
            a = 0

    except:
        a = 5
        print("获取订单信息错误,请联系管理员 open_orders")

    return a

def duo_kai():
    #balance_exchange = bitfinex.fetch_balance()  # 获取exchange账户资产
    # 下单参数

    amount = kaichang_zhongshu

    print("发出 exchange买多委托")
    order_info = bitfinex.create_limit_buy_order(symbol, amount, pirce, {'type': 'exchange limit'})  # margin买单

    #返回委托编号
    weituo_bianhao = order_info['id']

    print("发出开多工单,返回编号")
    print(weituo_bianhao)
    sleep(30 * 1)

    return weituo_bianhao

def duo_pin():
    print("多头平仓开始 duo pin 函数内")


    amount = kaichang_zhongshu - (kaichang_zhongshu*0.003)
    order_info = bitfinex.create_market_sell_order(symbol, amount, {'type': 'exchange market'})  # margin买单

    #返回委托编号
    weituo_bianhao = order_info['id']

    print("发出开多工单,返回编号")
    print(weituo_bianhao)
    sleep(30 * 1)
    return weituo_bianhao

def kong_kai():

    #委托笔数 赋值 (买多是股/量)
    amount = kaichang_zhongshu

    print("委托卖空数量")
    print("amount")


    print("发出 卖空委托")
    order_info = bitfinex.create_limit_sell_order(symbol, amount, pirce_kong, {'type': 'limit'})  # margin卖单
    #print( order_info)
    #print(order_info['id'])

    #返回交易编号
    weituo_bianhao = order_info['id']

    print("已经发出卖空工单,返回编号 等待30秒")
    print(weituo_bianhao)
    sleep(30 * 1)

    return weituo_bianhao

def kong_pin():
    print("空头平仓开始 kong pin 函数内")

    #这里应该获取已知仓位数
    amount = kaichang_zhongshu - (kaichang_zhongshu*0.003)

    order_info = bitfinex.create_market_buy_order(symbol, amount, {'type': 'market'})  # margin买单
    #委托空平已经结束

    #返回委托编号
    weituo_bianhao = order_info['id']

    print("发出开多工单,返回编号")
    print(weituo_bianhao)
    sleep(30 * 1)
    # 此处是否应该同时返回 是否成交,因为是市价单
    return weituo_bianhao





# 程序目录下生成文件txt_in_001.json
"""
[{
"datetime_in":"2018-09-17 09:00",
"symbol_in":"eosusd",
"close_latest":5.05,
"mp_latest":0,
"mp_old":0,
"amount_latest":5,
"amount_old":0,
}]

目前用到的交易的参数是
"mp_latest":0,
"mp_old":0,



解释如下:

空仓状态
"mp_latest":0,
"mp_old":0,

#多
首次发出看多信号,准备开多头买单
"mp_latest":1,
"mp_old":0,

已经成功开多,目前是多头持仓
"mp_latest":1,
"mp_old":1,

发出多头平仓信号,准备平多头
"mp_latest":0,
"mp_old":1,



#空
发出空头信号, 准备开空单
"mp_latest":-1,
"mp_old":0,

#目前已经是空头,有空头仓位
发出空头信号, 准备开空单
"mp_latest":-1,
"mp_old":-1,

#发出空头平仓信号,准备平空头仓位
发出空头信号, 准备开空单
"mp_latest":0,
"mp_old":-1,


"""
#!!!!!!!!!!!!!!!!!
#!!!注意 jion文件内 切换到 多头平仓和空头平仓时候要小心, 因为这个是一市价来执行的
#!!!!!!!!!!!!!!!!



while True:
    try:
        data_str = open('txt_in_001.json').read() #linux可能需要添加./
    except:
        print("读取来源文件出错,请联系管理员,10秒后再次尝试")
        sleep(10 * 1)
        continue



    df = pd.read_json(data_str)

    print(type(df))
    print(df)
    print("策略来源日期时间: " + df['datetime_in'][0])
    print("策略交易品种: " + df['symbol_in'][0])
    print("策略最近价格: " + str(df['close_latest'][0]))
    print("策略仓位方向 最新: " + str(df['mp_latest'][0]))
    #用到
    print("策略仓位方向 前一根K: " + str(df['mp_old'][0]))
    #用到
    print("策略仓位数量 最新: " + str(df['amount_latest'][0]))
    print("策略仓位数量 前一根: " + str(df['amount_old'][0]))






    #空仓
    if df['mp_latest'][0]==0 and df['mp_old'][0]==0:
        print("空仓 mp=0; mp[-1] = 0目前无买入卖出信号,10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #print("检查EOS实盘仓位")
        #空仓检查
        #changwei_jiancha

        print("委托编号归零处理")
        weituo_bianhao = 0

    # 多头开仓++
    elif df['mp_latest'][0]==1 and df['mp_old'][0]==0:
        print("多开+++mp=1; mp[-1] = 0 发出 开仓 多头信号 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #仓位检查
        changwei = changwei_jiancha()

        if changwei >1 and mp_local == 1:
            print("账户中已经有多头仓位了,无需再次开仓")


        elif changwei<1:
            # 确认实盘没有仓位准备开仓 等待10秒后
            #多头开仓
            sleep(5)
            shishi_changwei = open_orders()
            print("显示 未成交的订单 返回999:有此策略订单, 0无此策略订单或当前无订单 5默认值")
            print(shishi_changwei)

            sleep(5)
            #查询订单信息

            print("最新 委托-成交编号")
            print("weituo_bianhao")
            print(weituo_bianhao)


            if weituo_bianhao !=0:

                #返回订单状态,检查是否在委托单中
                order_info = bitfinex.fetch_order(id=weituo_bianhao, symbol='BTC/USD')
                print(order_info['status'])

                weituo_zhuangtai = order_info['status']
                print(weituo_zhuangtai)


                #'open', 'closed', 'canceled'

            if  weituo_zhuangtai == 'open':
                print("符合 open, 已经发出此策略委托单,请等待")
                print(weituo_zhuangtai)
                mp_local = 1

            elif weituo_zhuangtai  == 'closed':
                print("此订单已经成交了")
                mp_local = 1


            elif shishi_changwei == 999:
                print("符合精度, 已经发出此策略委托单,请等待")
                mp_local = 1

            elif shishi_changwei == 5:
                print("订单状况不明,请联系管理员")

            elif shishi_changwei == 0:
                print("准备开仓, 无订单或者订单非此策略,")
                print("检查 是否已经存在仓位,已经成交,")
                if weituo_zhuangtai == 'closed':
                    print("开多 订单已经成交,无需开仓")
                    mp_local = 1

                else:
                    print("准备 多头开仓")
                    #开仓 同时返回 交易编号

                    try:
                        print("正在 多头开仓")
                        weituo_bianhao =  duo_kai()
                        mp_local = 1
                        print("成功开仓")

                    except:
                        print("开仓遇到问题..请联系管理员")


            else:
                print("委托数量返回异常,请联系管理员")
                sleep(5)
                #接下来要检查 已经成交的仓位,是否包含

    # 多头持仓
    elif df['mp_latest'][0] == 1 and df['mp_old'][0] == 1:
        print("多持仓 mp=1; mp[-1]=1 多头信号 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # print("检查实盘仓位")
        # changwei_jianchang()

        # 此时委托编号归零处理
        print("委托编号归零处理")
        weituo_bianhao = 0

    #多头平仓+-
    elif df['mp_latest'][0]==0 and df['mp_old'][0]==1:
        print("多平---mp=0; mp[-1]=1 发出 平仓 多头信号 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #changwei_jiancha()

        if weituo_bianhao != 0:
            # 返回订单状态,检查是否在委托单中
            order_info = bitfinex.fetch_order(id=weituo_bianhao, symbol='BTC/USD')
            print(order_info['status'])
            weituo_zhuangtai = order_info['status']
            print(weituo_zhuangtai)

            # 'open', 'closed', 'canceled'

        if weituo_zhuangtai == 'open':
            print("多头平仓已经在订单列表 符合 open, 请等待成交")
            print(weituo_zhuangtai)
            mp_local = 0
        elif weituo_zhuangtai == 'closed':
            print("多头平仓已经成交,不需要再平仓")
            print(weituo_zhuangtai)
            mp_local = 0

        # elif weituo_zhuangtai == 'canceled':
        #     print("多头平仓单已经撤单,是否需要再次平?")
        #     print(weituo_zhuangtai)
        #     mp_local = 0
        else:

            try:
                print("多头 准备市价平仓")

                #返回订单编号
                weituo_bianhao = duo_pin()
                print("多头 市价平仓完毕")
                mp_local = 0


            except:
                print("多头平仓遇到问题..请联系管理员")


    ### 空头开始

    #空头开仓 --
    elif df['mp_latest'][0] == -1 and df['mp_old'][0] == 0:
        print("空头 开仓 mp=-1; mp[-1] = 0 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 仓位检查
        changwei_margin = changwei_jiancha_margin()
        print(changwei_margin)
        #此处代码需要进一步修改

        a_temp = 0

        #changwei_margin > 1 and
        if mp_local == 10:
            print("实盘已经有空头仓位了,无需再次开仓")


        elif a_temp < 1:
            # 确认实盘没有仓位准备开仓 等待10秒后
            # 多头开仓
            #sleep(5)

            shishi_changwei = open_orders()
            print("显示 实时委托状态 返回999:有此策略订单, 0无此策略订单或当前无订单 5默认值")
            print(shishi_changwei)
            print("shishi_changwei 显示了吗")
            sleep(5)


            # 查询订单信息

            print("最新 委托-成交编号")
            print("weituo_bianhao")
            print(weituo_bianhao)

            if weituo_bianhao != 0:

                # 返回订单状态,检查是否在委托单中

                try:
                    order_info = bitfinex.fetch_order(id=weituo_bianhao, symbol='BTC/USD')
                    print(order_info['status'])

                    weituo_zhuangtai = order_info['status']
                    print(weituo_zhuangtai)

                except:
                    print("根据定点编号查找 委托出错出错 此处很危险,是否考虑跳出程序")
                    print("终止程序 通知管理员")



                # 'open', 'closed', 'canceled'

            if weituo_zhuangtai == 'open':
                print("符合 open, 已经发出此策略委托单,请等待")
                print(weituo_zhuangtai)
                mp_local = -1

            elif weituo_zhuangtai  == 'closed':
                print("卖空 订单已经成交了")





            elif shishi_changwei == 999:
                print("符合精度, 已经发出此策略委托单,请等待")
                mp_local = -1

            elif shishi_changwei == 5:
                print("订单状况不明,请联系管理员")

            elif shishi_changwei == 0:
                print("准备开仓, 无订单或者订单非此策略,")
                print("检查 是否已经存在仓位,已经成交,")
                if weituo_zhuangtai == 'closed':
                    print("此订单已经成交,无需开仓")
                    mp_local = 1

                else:
                    print("准备 空头开仓")
                    # 开仓 同时返回 交易编号

                    try:
                        print("正在空头开仓")
                        weituo_bianhao = kong_kai()
                        mp_local = -1
                        print("成功 空头开仓")
                    except:
                        print("空头开仓遇到问题..请联系管理员")


    # 空头持仓
    elif df['mp_latest'][0] == -1 and df['mp_old'][0] == -1:
        print("空头持仓 mp=-1; mp[-1]=-1 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 此时委托编号归零处理
        print("委托编号归零处理")
        weituo_bianhao = 0


    #空头平仓+-
    elif df['mp_latest'][0]==0 and df['mp_old'][0]==-1:
        print("空平---mp=0; mp[-1]=-1 发出 平仓")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #changwei_jiancha()
            #这里防止刚挂出平仓单,在订单中还未成交,又重复挂点,
            #委托编号不为0 说明现在有委托单,进一步检查

        if weituo_bianhao != 0:
            # 返回订单状态,检查是否在委托单中
            order_info = bitfinex.fetch_order(id=weituo_bianhao, symbol='BTC/USD')
            print(order_info['status'])
            weituo_zhuangtai = order_info['status']
            print(weituo_zhuangtai)

            # 'open', 'closed', 'canceled'

        if weituo_zhuangtai == 'open':
            print("空头平仓已经在订单列表 符合 open, 请等待成交")
            print(weituo_zhuangtai)

        elif weituo_zhuangtai == 'closed':
            print("空头平仓已经成交,不需要再平仓")
            print(weituo_zhuangtai)
            mp_local = 0

        # elif weituo_zhuangtai == 'canceled':
        #     print("多头平仓单已经撤单,是否需要再次平?")
        #     print(weituo_zhuangtai)
        #     mp_local = 0
        else:

            try:
                print("空头 准备市价平仓")

                #返回订单编号

                #print("模拟空平")
                weituo_bianhao = kong_pin()
                print("空平 市价平仓完毕")
                mp_local = 0


            except:
                print("空头平仓遇到问题..请联系管理员")



    else:
        print("来源json 发生其他情况,请联系管理员 10秒后再次检查")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        changwei_jiancha()


    sleep(15 * 1)






