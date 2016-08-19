# -*- coding: utf-8 -*-

"""
Created on Fri Jun 03 14:41:30 2016
@author: 苑广山
@Email: yuanguangshan@163.com

本模块实现如下功能：
1. oneCode:获取客户输入的单一windcode
2. windCode:一次性获得客户输入的多个windcode;
3. getCodeFromClipboard:通过剪切板获得用户复制到剪切板上的wind代码；
4. getCodes：利用正则表达式获取客户剪切板中的多个代码；
5.  getWindCodes：利用正则表达式获取客户剪切板中的多个代码（wind品种指数；
6. getClipboard：获取剪切板数据；
7. setClipboard：设置剪切板数据；
8. getActivecodes：从具体合约代码获取主力合约代码

"""

import re
#import win32clipboard as wc
#import win32con
from WindPy import *
from pandas import Series, DataFrame

w.start()  # 启动wind接口

def oneCode():
    '获取用户输入的单一windcode，如cu.shf(行情）,S15458785(EDB)'

    code = input('Please input a code:')
    return code


def windCode():
    '逐一获取用户输入的edb代码，并合为一个字符串，用于通过wind python接口提取数据'

    codes = []
    c = 's5707135'

    while True:
        edb_code = input(r"EDB code:")
        if edb_code != "":
            codes.append(edb_code)
        else:
            break
    codes = ','.join(codes)
    return c if len(codes) == 0 else codes


def getCodeFromClipboard():
    '通过剪切板获得用户复制到剪切板上的edb代码，利用这些代码来调用接口获取数据'
    d = getClipboard()
    codes = re.findall('[SM]+\d{7}', str(d))
    return codes


def getClipboard():
    '获取剪切板中的数据'
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    data = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return data


def setClipboard(aString):
    '设置剪切板中的数据'
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
    '利用正则表达式获取客户剪切板中的多个代码（wind商品品种指数，如RUFI.WI）'
    d = getClipboard()
    codes = re.findall('[A-Za-z]{3,4}\.WI', str(d))
    return codes


def getActivecodes():
    '具体期货合约代取获取wind主力合约代码，如ru1609.shf返回ru.shf'
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
