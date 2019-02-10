# _*_ coding:utf-8 _*_

#import pandas as pd
from time import sleep
import datetime
import os
import json
import time
from dateutil import parser
import ccxt

#备注 开仓多少只用到 json文件中的 "duokong_all_new",

#"duokong_all_old" 这行没有用的
      
      
      
# nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


#dingding
#from datetime import datetime
import requests
import warnings
warnings.filterwarnings("ignore")


#read json 不使用pandas


#pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

#eos_chang_12
#bit_eth-dyn_chang_online_16
# # =====创建bitfinex交易所
bitfinex = ccxt.bitfinex()
bitfinex.apiKey = ''
bitfinex.secret = ''






# =====获取bitfinex账户资产
# balance_exchange = bitfinex.fetch_balance()  # 获取exchange账户资产
# print(balance_exchange['info'])
# print(balance_exchange['free'])
# print(balance_exchange['used'])
# print(balance_exchange['total'])

s_name = " test_1 "

symbol_name = "tEOSUSD"


# =====下单交易
# 下单参数
#symbol = 'EOS/USD'
symbol = 'EOS/USD'


#本程序虚拟 仓位增加数量


#每次开仓单位数量
kaichang_shuliang = 10

#杠杆倍数
ganggan_shuliang = 1


#最大开仓数量
max_mp = 13


json_path = "EOS.json"
#如果不在同一目录就改 json_path = "C:/phpStudy/WWW/json/EOS.json"

error_log_file = "online_3_bit_error_log_file.txt"

save_wss_error_log = "online_3_bit_save_wss_error_log.txt"







# 限价单
#order_info = bitfinex.create_limit_buy_order(symbol, amount, pirce, {'type': 'limit'})  # margin买单
# order_info = bitfinex.create_limit_sell_order(symbol, amount, pirce, {'type': 'limit'})  # margin卖单

#print(order_info)

# 市价单，市价单不需要输入价格
#order_info = bitfinex.create_market_buy_order(symbol, amount, {'type': 'market'})  # margin买单
# order_info = bitfinex.create_market_sell_order(symbol, amount, {'type': 'market'})  # margin买单



# ===发送钉钉消息，id填上使用的机器人的id
def send_dingding_msg(content, robot_id='xxxxxxxxxxxxxxxxxxxx'):
    try:
        msg = {
            "msgtype": "text",
            "text": {"content": content + '\n' + datetime.datetime.now().strftime("%m-%d %H:%M:%S")}}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id
        body = json.dumps(msg)
        requests.post(url, data=body, headers=headers)
        print('成功发送钉钉')
        #https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxx
        
    except Exception as e:
        print("发送钉钉失败:", e)







def read_json(local_json_path):

    try:
        with open(local_json_path, 'r') as f:
            df = json.loads(f.read())

        print(df)

        datetime_in = df["datetime_in"]

        symbol_in = df["symbol_in"]

        price = df["price"]

        #获取最新仓位
        duokong_all_new = df["duokong_all_new"]

        # 获取前一次仓位
        duokong_all_old = df["duokong_all_old"]

        
        #
        yesno = df["yesno"]
        
        
        open_date = df["open_date"]
        
        open_netop = df["open_netop"]
        
        
        now_netop_zijin = df["now_netop_zijin"]
        
        


        print("显示json文件内容")
        print(f"策略来源日期时间: {datetime_in}")
        print(f"策略交易品种: {symbol_in}")
        print(f"策略最近价格: {price}")
        print(f"策略仓位 最新: {duokong_all_new}")
        print(f"策略仓位 前一次: {duokong_all_old}")
        print(f"yesno: {yesno}")
        print(f"开始时间pro: {open_date}")
        print(f"开始权益pro: {open_netop}")
        print(f"最新权益: {now_netop_zijin}")

    except:
            print("读取来源文件出错,请联系管理员,10秒后再次尝试")
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + "读取来源文件出错,请联系管理员,10秒后再次尝试"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()


    return datetime_in, symbol_in, price, duokong_all_new, duokong_all_old
    #return datetime_in




#读取 json文件
#read_json()

#print("read_json() OK")
#atetime_j, symbol_j, price_j, mp_new, mp_old = read_json(json_path)

#print(datetime_j, symbol_j, price_j, mp_new, mp_old)



#先初始化 mp_local 虚拟仓位,使得每次启动程序 初始化仓位始终等于来源json的最新持仓
#这样可以避免开启python后自动加仓位
#此处不会进入循环


try:
    #运行 read_json() 读取json文件,并且导出
    

    t_datetime_j, t_symbol_j, t_price_j, mp_local, t_mp_old = read_json(json_path)

    #字符串转数字
    mp_local = int(mp_local)

    print(f"初始化仓位>>>: {mp_local}")

    print("请人工确认初始化仓位数量是否正确")
    print("如果不符合你预期,请进入网站手动加减仓位")
    print("正常情况,程序运行后会复制json文件最新仓位")
    print("也就是说,每次启动时不会去加减仓位,有信号后才会操作")


    print("!输入yes继续, 输入no退出")


    yesno = input()

    if yesno == "yes":
        pass
    elif yessno =="no":
        exit()

    else: 
        exit()


except Exception as e: 
    print("运行函数 read_json() 错误, 请检查json文件,通知管理员,程序即将终止")
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_wss_error_log = str(nowTime) + "---" + str(e) + "运行函数 read_json() 错误, 请检查json文件,通知管理员,程序即将终止"
    file_handle=open(error_log_file,'a',encoding='utf-8')
    #file_handle.write()
    print("开始写入错误日志")
    file_handle.write(save_wss_error_log + '\n')
    file_handle.close()
    print("写入日志正常")

    exit()



# ===获取bfx交易所margin账户和仓位信息
def fetch_account_info(exchange, base_coin, trade_symbol):
    """
    获取账户信息
    :param exchange: 交易所
    :param base_coin: 基准币的名称
    :param trade_symbol: 交易对的名称
    :return:
    :param account_info: dict形式，包含账户和仓位信息
    """
    # 创建用于存放账户信息的变量
    account_info = {'仓位数量': 0, '仓位成本': 0, '仓位利润': 0, '仓位爆仓价格': 0}

    while True:

        # 获取账户的资产信息
        try:
            data = exchange.private_post_auth_r_wallets()  # 从bfx交易所获取账户balance信息
        except Exception as e:
            send_dingding_msg('获取账户信息失败')
            print(e)
            continue
            
            
        """
            
        data = pd.DataFrame(data, columns=['交易账户', '币种', '数量', 'unknow', 'unknow2'])  # 将数据转化为df格式
        condition1 = data['交易账户'] == 'margin'
        condition2 = data['币种'] == base_coin
        account_info['账户保证金'] = float(data.loc[condition1 & condition2, '数量'])

        # 获取账户的margin持仓信息
        try:
            position_info = exchange.private_post_auth_r_positions()  # 从bfx交易所获取账户的持仓信息
        except Exception as e:
            send_dingding_msg('获取持仓信息失败')
            print(e)
            continue
        print(position_info)
        if len(position_info) > 0:  # 当持仓信息信息不为空时
            position_info = pd.DataFrame(position_info, columns=['交易对', '状态', '持仓量', '成本价格', '借币利息',
                                                                 'unknow1', '利润', 'unknow2', '爆仓价格',
                                                                 'unknow3'])  # 将数据转化为df格式
            condition1 = position_info['交易对'] == ('t' + str(trade_symbol))
            position_info = position_info.loc[condition1, :]
            if len(position_info) > 0:
                account_info['仓位数量'] = float(position_info.iloc[0]['持仓量'])
                account_info['仓位成本'] = float(position_info.iloc[0]['成本价格'])
                account_info['仓位利润'] = float(position_info.iloc[0]['利润'])
                account_info['仓位爆仓价格'] = float(position_info.iloc[0]['爆仓价格'])

        break


    """
    
    aaa = "aaa"
    
    return aaa














####初始化虚拟仓位结束


#循环程序开始运行

while True:

    try:
        #运行 read_json() 读取json文件,并且导出
        sleep(3)
        datetime_j, symbol_j, price_j, mp_new, mp_old = read_json(json_path)
        #read_json()
        print("read_json() OK")
        
        price_j = float(price_j)
        mp_new = int(mp_new)
        mp_old = int(mp_old)

        print(datetime_j, symbol_j, price_j, mp_new, mp_old)


    except Exception as e: 
        print("运行函数 read_json() 错误, 请检查json文件,通知管理员,程序即将终止")
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_wss_error_log = str(nowTime) + "---" + str(e) + "运行函数 read_json() 错误, 请检查json文件,通知管理员,程序即将终止"
        file_handle=open(error_log_file,'a',encoding='utf-8')
        #file_handle.write()
        print("开始写入错误日志")
        file_handle.write(save_wss_error_log + '\n')
        file_handle.close()
        print("写入正常")
        continue






    #对来源文章时间进行验证,如何两者相差10分钟,程序肯定出问题,需要通知管理员

    #time_a = "2018/9/21 21:03:01."

    print(f"json 时间: {datetime_j}")

    localtime = time.strftime("%Y/%m/%d  %X ")
    print(f"本机时间:  {localtime}")
    datetime_struct = parser.parse(datetime_j)

    #获取json文件内的unix时间
    time_json_unix = time.mktime(datetime_struct.timetuple())
    #print(f"json unix time {time_json_unix}")
    #print(type(time_unix_json))

    #获取本机当前的unix时间
    time_local_unix = time.time()
    #rint(f"local unix time {time_local_unix}")
    #print(type(time_unix_now))   

    try:
        #时间检验开始
        if  (time_local_unix - time_json_unix) >600000000 or (time_json_unix - time_local_unix >600000000):
            print("!!!警告!!!本机时间和json文件时间相差10分钟以上,请联系管理员")
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + "!!!警告!!!本机时间和json文件时间相差10分钟以上,请联系管理员"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()
            print("写入正常")
            '''
            #如果本地unix时间和json时间相差10分钟,说明来源出问题,或本机有问题,
            # 需要终止运行程序,并且通知管理员.
        
            '''
            continue
            


        else: 
            print("时间检查通过,进行下一步工作")
            

    except Exception as e: 
        print("时间执行程序出错")  
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_wss_error_log = str(nowTime) + "---" +str(e) + "时间执行程序出错"
        file_handle=open(error_log_file,'a',encoding='utf-8')
        #file_handle.write()
        print("开始写入错误日志")
        file_handle.write(save_wss_error_log + '\n')
        file_handle.close()
        print("写入正常")
        continue



    #交易名字对比
    print("开始检验交易商品名")
    try:
        if symbol_name != symbol_j:
            print("来源json内包含的商品和和本程序不符合,请联系管理员")
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + "来源json内包含的商品和和本程序不符合,请联系管理员"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()
            continue
        
        else: 
            print("时间检查通过,进行下一步工作")
    except Exception as e:   
        print("交易商品校验出错请,请联系管理员")  
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_wss_error_log = str(nowTime) + "---" + str(e) +"交易商品校验出错请,请联系管理员"
        file_handle=open(error_log_file,'a',encoding='utf-8')
        #file_handle.write()
        print("开始写入错误日志")
        file_handle.write(save_wss_error_log + '\n')
        file_handle.close()
        print("写入正常")
        continue


    print("本次需要增加的数量")


    print(f"这里的 mp_local: {mp_local}")
    print(f"这里的mp_new : {mp_new}")

    mp_renew2 = mp_new - mp_local

    print("计算更新思路 renews2")
    print(f"mp_renew2 : {mp_renew2}")


    print("完成来源文件时间和商品名称检验过程")
    print("++++开始进行交易环节++++")



    if mp_new == mp_local:
        print("本地虚拟仓位和最新仓位保持一致,无需任何行动")
        
        print(f"目前虚拟仓位数: {mp_local}")

        print(f"目前json仓位数量: {mp_new}")

        print("将继续访问来源json文件")
        sleep(0.1)
        continue

    elif mp_local >30 or mp_new>30 or (mp_local >0 and mp_local<1):
        print("mp_local")
        print("error !!!虚拟仓位数量发生异常情况 大于30,请检查原因,问题很严重")
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_wss_error_log = str(nowTime) + "---" + "error !!!虚拟仓位数量发生异常情况 大于100"
        file_handle=open(error_log_file,'a',encoding='utf-8')
        #file_handle.write()
        print("开始写入错误日志")
        file_handle.write(save_wss_error_log + '\n')
        file_handle.close()
        print(f"此时的 mylocal 虚拟仓位: {mp_local}")


        continue


    elif abs(mp_renew2) > max_mp*2 or abs(mp_new) > max_mp:

        try:
            mp_local == 0.5

            print(f"显示json文件本次新增数量 mp_renew {mp_renew2}")
            print(f"显示json文件最新持仓数量 mp_new {mp_new}")
            print(f"显示程序最大开仓数量 mp_new {max_mp}")
            print(f"此时  my_local {mp_local}")
            print(f"新增开仓数量  {mp_renew2} 超过最大开仓数量的两倍  {max_mp},或者 mp_new>max_mp ")
            print(f"error !!!mp_renew 严重出错,请联系管理员!!!")
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + "error !!!mp_renew 严重出错,请联系管理员!!!"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()

            print(f"此时的 mylocal 虚拟仓位: {mp_local}")
            
            continue
        except: 
            print("出现异常情况")
            continue

    else: 
        print("开始买卖环节 ")
        



        try:
            print("发出交易信号 开始....")

            #这个应该建立一个检查连接,说明与服务器正常连接
            #比如判断 key是否错误,或者连接中断等


            #前期准备工作

            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"发出交易信号 开始.. 当前时间: {nowTime}")
            # ### example new order
            # if counter == 5:

            print(f"当前信号 mp_renew开仓数: {mp_renew2}")
            print(f"当前信号 mp_local虚拟开仓数: {mp_local}")


            #计算实际开仓数量
            all_kaichang_shuliang = float(kaichang_shuliang*ganggan_shuliang*mp_renew2)


            #每次开仓单位数量
            #kaichang_shuliang

            #杠杆倍数
            #ganggan_shuliang

            #程序调试时候时候,时间为市价 单或者 价格上浮10%
            buy_price_j = price_j*0.9  #多单委托价格

            sell_price_j = price_j*1.1 #空单委托价格


            #price_j 来自于 来源文档json
            #buy_price_j = price_j*1.05

            #sell_price_j = price_j*0.95





            print(f"多单委托价格 buy_price_j: {buy_price_j}")
            print(f"空单委托价格 sell_price_j: {sell_price_j}")
            print(f"准备开仓数: all_kaichang_shuliang: {all_kaichang_shuliang}")

        except Exception as e:
            print("准备开仓前准备出错,请联系管理员")
            print(e)
            sleep(5)
            continue



        #符合买卖前 是否先查询数据






        #进入买卖阶段
        

       

        try: 
            if all_kaichang_shuliang >0:
                #准备开多单
                #exch_order = self.mywss.new_order("LIMIT", symbol_name, all_kaichang_shuliang_str, buy_price_j)
                print("准备发多单")
                                                
                nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"委托单开始发出时间: {nowTime}")
                
                try:     
                    print("开始 发出多单委托")
                 

                    order_info = bitfinex.create_limit_buy_order(symbol, all_kaichang_shuliang , buy_price_j, {'type': 'limit'})  # margin买单

                    print("结束 发出多单委托")

                    mp_local = mp_new    

                    sleep(1)

                    print(f"打印多单委托情况: {order_info}")

                    print("多单已经发出,调整虚拟仓位")
                    

                    print(f"mp_local:{mp_local}")

                    print(f"mp_local:{mp_new}")

                    print("结束 虚拟仓位赋值")
                    print("程序等待5秒")
                    
                    
                                
                    send_dingding_msg(f"{s_name} 交易成功")
                    send_dingding_msg(f"{symbol} {all_kaichang_shuliang} {buy_price_j}")
        
        
                    sleep(5)

                except Exception as e:
                    print("多头委托单发生异常!,可能已经发出,返回错误,也可以没有发出")
                    print("赋值 程序虚拟仓位50,以避免重复开仓")

                    #上面多单发生未知错误,除了联系管理员外,假设已经开仓成功
                    mp_local = mp_new


                    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_wss_error_log = str(nowTime) + "---" + str(e) + "---" + "多头委托单发生异常!,可能已经发出,返回错误,也可以没有发出"
                    file_handle=open(error_log_file,'a',encoding='utf-8')
                    #file_handle.write()
                    print("开始写入错误日志")
                    file_handle.write(save_wss_error_log + '\n')
                    file_handle.close()
                    print("写入正常")
                    
                    
                    send_dingding_msg(f"{s_name} 多头策略出错")
                    send_dingding_msg(str(e))
            
            
                    continue



        except Exception as e:
            mp_local = 0.5
            print("多头委托单发生异常!,可能已经发出,返回错误,也可以没有发出")
            print("赋值 程序虚拟仓位50,以避免重复开仓")
            
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + str(e) + "---" + "多头委托单发生异常!,可能已经发出,返回错误,也可以没有发出"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()
            print("写入正常")
            
            send_dingding_msg(f"{s_name} 多头委托单发生异常!,可能已经发出,返回错误,也可以没有发出")
            send_dingding_msg(str(e))
            
            
            print("sleep 20")
            sleep(20)
            continue
        


        
        
        try: 
            if all_kaichang_shuliang <0:
                #准备开空单
                print("准备发空单")

                nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"委托单开始发出时间: {nowTime}")
                
                try:     
                    print("开始 发出空单委托")
                    #order_info = bitfinex.create_limit_buy_order(symbol, all_kaichang_shuliang , buy_price_j, {'type': 'limit'})  # margin买单

                    #这里和wss bitf 不同, 数量不是负的
                    order_info = bitfinex.create_limit_sell_order(symbol, (0-all_kaichang_shuliang) , sell_price_j, {'type': 'limit'})  # margin买单
                    # order_info = bitfinex.create_limit_sell_order(symbol, amount, pirce, {'type': 'limit'})  # margin卖单


                    print("结束 发出空单委托")

                    mp_local = mp_new

                    print(f"打印空单托情况: {order_info}")

                    print("空单已经发出,调整虚拟仓位")
                    

                    print(f"mp_local:{mp_local}")

                    print(f"mp_local:{mp_new}")

                    print("结束 虚拟仓位赋值")
                    print("程序等待5秒")
                    
                    send_dingding_msg(f"{s_name} 交易成功")
                    send_dingding_msg(f"{symbol} {all_kaichang_shuliang} {buy_price_j}")
                    
                    
                    sleep(5)

                except Exception as e:

                    print("打印异常")
                    print(e)

                    print("空头委托单发生异常!,可能已经发出,返回错误,也可以没有发出")
                    print("赋值 程序虚拟仓位50,以避免重复开仓")

                    #上面多单发生未知错误,除了联系管理员外,假设已经开仓成功
                    mp_local = mp_new
                    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_wss_error_log = str(nowTime) + "---" + str(e) + "---" + "空头委托单发生异常!,可能已经发出,返回错误,也可以没有发出"
                    file_handle=open(error_log_file,'a',encoding='utf-8')
                    #file_handle.write()
                    print("开始写入错误日志")
                    file_handle.write(save_wss_error_log + '\n')
                    file_handle.close()
                    print("写入正常")
                    
                    
                    send_dingding_msg(f"{s_name} 空头策略出错")
                    send_dingding_msg(str(e))
            
            
            
                    continue


        except Exception as e:
            #交易发生异常,依旧赋值50,以免重复开单
            mp_local = 0.5

            print("error 交易发生异常!!!!!!!!!")     
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_wss_error_log = str(nowTime) + "---" + str(e) + "---" + "error 交易发生异常!!!!!!!!!"
            file_handle=open(error_log_file,'a',encoding='utf-8')
            #file_handle.write()
            print("开始写入错误日志")
            file_handle.write(save_wss_error_log + '\n')
            file_handle.close()
            print("写入日志正常")

            send_dingding_msg(f"{s_name} error 交易发生异常!!!!!!!!!")
            send_dingding_msg(str(e))
            
            
            print("sleep 20")
            sleep(20)
            
            continue

           


           


        # symbol_name = "tEOSUSD"

        #     #exch_order = self.mywss.new_order_stop_limit("STOP LIMIT", "tEOSUSD", "-3", "4","3.9")
        #     print(f"new order is {exch_order}")

        sleep(1)
