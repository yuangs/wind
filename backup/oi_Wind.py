import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from WindPy import *
from wind.tools import downloader

w.start()
def oi(startdate='2012-7-29',enddate='2013-7-29',varity='rb.shf',wind_code='all',member_name='all',order_by='long'):
    '''利用万得数据接口获取得品种机构龙虎榜数据，类似于万得F9持仓分析'''
    #构造参数
    startdate =startdate
    enddate = enddate
    varity = varity
    wind_code = wind_code
    member_name = member_name
    order_by = order_by
    para1="futureoi"
    para2="startdate=%s;enddate=%s;varity=%s;wind_code=%s;\
    member_name=%s;order_by=%s" %(startdate,enddate,varity,wind_code,member_name,order_by)
    #获取万得期货持仓数据
    data=w.wset(para1,para2)
    #将万得的数据结构转化为pandas数据结构并返回
    ErrorCode = data.ErrorCode
    Codes = data.Codes
    Fields = data.Fields
    Times = data.Times
    Data = data.Data
    # index=data[0]
    df = pd.DataFrame(Data).T
    df.columns = Fields
    print('期货机构持仓情况如下：')
    # print(df)
    print(df.shape)
    # df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\oi.csv", header=False)
    return df

def gethistoi(n=12,member_name='永安期货'):
    '''利用万得数据接口获取某家期货公司的历史持仓'''
    # startdate =datetime.datetime.now()-timedelta(30*n)
    # enddate =datetime.datetime.now()
    data=[]
    while n>0:
        startdate = datetime.now() - timedelta(30 * n)
        enddate =datetime.now()-timedelta(30 * n-30)
        d1="%s" % startdate.date()
        d2="%s" % enddate.date()
        df=oi(startdate =d1,enddate = d2,member_name=member_name)
        n=n-1
        data.append(df)
        # with open(r"C:\Users\gsyuan\Desktop\Wind Data\oi.csv",mode='a') as f:
        #     df.to_csv(f,header=False)
        print(df.date)
    df = pd.concat(data).drop_duplicates(subset='date',keep=False)
    df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\oi.csv", header=False)


#交易所数据源
def cffexoi(date='0811'):
    date = date
    url = 'http://www.cffex.com.cn/fzjy/ccpm/2016%s/%s/IF_1.csv' % (date[0:2], date[-2:])
    downloader(url)

def shfeoi():
    dates = ['20160104', '20160105']
    for date in dates:
        url = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat' % date
        downloader(url)


# oi(startdate='2015-4-5',enddate='2016-6-6',member_name='永安期货')


if __name__ == '__main__':
  oi()
  gethistoi(n=12)
