# -*- coding: utf-8 -*-

"""
Created on Fri Jun 03 14:41:30 2016
@author: 苑广山
@Email: yuanguangshan@163.com

本模块实现如下功能：
1、由用户通过键盘输入edb指标的id（不带前缀s),可输入任意多个edb指标，提取数据到指定的
csv文件；
2、用户也可用excel一次性导出多个edb指标的id，并复制到剪切贴上，模块会自动提取代码并
取数据；
3、输入截止日期由用户输入，如果不输入，采用默认值;

"""

import pandas as pd
import datetime
import re
from WindPy import *
from pandas import Series, DataFrame
from constants import cons

w.start()  # 启动wind接口

# 如果用户不输入任何指标，则用这个默认指标提取数据
# 如果用户不输入起始时间，则设置默认时间为s
# 如果用户不输入起始时间，则设置默认时间为e
# e=datetime.datetime.now().strftime('%y-%m-%d')
TRADEUNIT = cons.TRADEUNIT
def oneCode():
    '获取客户输入的单一windcode'

    code = input('Please input a code:')
    return code


def windCode():
    '逐一获取客户输入的edb代码，并合为一个字符串，用于通过wind python接口提取数据'

    codes = []
    c = 's5707135'

    while True:
        edb_code = input(r"EDB code:")
        if edb_code != "":
            # edb_code='s'+
            # edb_code,有些指标s或m都有指标（m0175593，sm0175593)，容易混淆，所以输入全部，不能只输入数字
            codes.append(edb_code)
        else:
            break
    codes = ','.join(codes)
    return c if len(codes) == 0 else codes


def getCodeFromClipboard():
    '''
    通过剪切板获得用户复制到剪切板上的edb代码，利用这些代码来调用接品获取数据
    '''
    d = getClipboard()
#  wc.OpenClipboard()
#  d = wc.GetClipboardData(win32con.CF_TEXT)
#  wc.CloseClipboard()
    codes = re.findall('[SM]+\d{7}', str(d))
    return codes


def getClipboard():
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    data = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return data


def setClipboard(aString):
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()
    return aString


def getCodes():
    '利用正则表达式获取客户剪切板中的多个代码'

    d = getClipboard()
    codes = re.findall('[A-Za-z]{1,2}\d{,4}\.[A-Za-z]{3,4}', str(d))
    return codes


def getWindCodes():
    '利用正则表达式获取客户剪切板中的多个代码（wind品种指数）'
    d = getClipboard()
    codes = re.findall('[A-Za-z]{3,4}\.WI', str(d))
    return codes


def getActivecodes():
    '将代码去除数字后返回，如ru1609.shf返回ru.shf'
    rawcodes = str(getCodes())
    s = re.sub('\d{3,4}', '', rawcodes)
    codes = setClipboard(s)
    codes = getCodes()
    return codes


def sDate():
    '''
    获得用户输入的开始日期
    '''
    sDate = input(r"Start date:")
    return '20120317' if sDate == "" else sDate


def eDate():
    '''
    获得用户输入的结束日期
    '''

    eDate = input(r"End date:")
    return '20160602' if eDate == "" else eDate


def edbSave():
    '获取客户剪切板中的edb代码，并调用接口获取edb指标的具体数据'

    # 获取客户剪切板中的代码及输入的起始与结束日期
    codes = getCodeFromClipboard()
    start = sDate()
    end = eDate()

    data = w.edb(codes, start, end, "Fill=Previous")
    datachg = [d.strftime('%y-%m-%d') for d in data.Times]
    df = DataFrame(data.Data, index=data.Codes, columns=datachg).T
    print('-' * 85)
    print(df)
    print('-' * 85)
    print('统计指标：')
    print(df.describe())
    print("sum", " " * 3, str(df.sum()).split(sep="    ")[1].rjust(10))
    return df


def future_info():
    '获得用户输入的某个期货合约的合约基本资料信息'

    codes = oneCode().upper()
    fields = "lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,\
  punit,changelt,mfprice,contractmultiplier,cdmonths,thours,ltdated,ddate,\
  ftmargins,trade_hiscode"
    beginTime = sDate()
    endTime = eDate()
    wsd = w.wsd(codes, fields, beginTime, endTime)
    df = pd.DataFrame(wsd.Data).T
    return df


def wset_sector():
    '通过windpy的接口获得数据，并用pandas处理数据并另存为csv文件'

    # wset格式：w.wset("sectorconstituent","date=2016-06-23;sectorid=
    # 1000019227000000")
    # 构造参数字符串
    p1 = "sectorconstituent"
    date = "=".join(['date', datetime.now().strftime('%Y-%m-%d')])
    sectorid = "=".join(['sectorid', input(r'input sectorid:')])
    p2 = ','.join([date, sectorid])
    # 提取数据
    wset = w.wset(p1, p2)
    # 将数据转化为pandas dataframe结构
    df = pd.DataFrame(wset.Data).T
    return df


def wset_futureoi():
    '通过windpy的接口获得数据，并用pandas处理数据并另存为csv文件'

    # wset格式：w.wset("sectorconstituent","date=2016-06-23;sectorid=
    # 1000019227000000")
    p1 = "futureoi"
    code = input('input code:')
    p = "startdate={0};enddate={1};varity={2};wind_code=all;member_name=all;order_by=long"
    p2 = p.format(sDate(), eDate(), code)
#  print(p1,p2)
    wset = w.wset(p1, p2)
    df = pd.DataFrame(wset.Data).T
    return df


def save(what):
    '将上述定义中的函数获取的数据保存到文件中'

    if what == 'sector':
        df = wset_sector()
        df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\\" + what + ".csv")
    elif what == 'oi':
        df = wset_futureoi()
        df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\\" + what + ".csv")
    elif what == 'edb':
        df = edbSave()
        df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\\" + what + ".csv")
    elif what == 'f_info':
        df = future_info()
        df.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\\" + what + ".csv")
    else:
        pass

if __name__ == '__main__':

    """
    测试持仓数据
    """
    print(getWindCodes())
