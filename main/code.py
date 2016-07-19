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

import re

#import win32clipboard as wc
#import win32con

from WindPy import *
from pandas import Series, DataFrame

w.start()  # 启动wind接口

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


if __name__ == '__main__':

    """
    功能测试
    """
    print(oneCode())
#    print(windCode())
    print(getCodeFromClipboard())
    print(getCodes())
    print(getWindCodes())
    print(getActivecodes())
