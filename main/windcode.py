# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:30:51 2016

@author: gsyuan
"""
import datetime
import re
from WindPy import *
w.start()


class windCode:
  '定义跟wind代码相关的操作类'
  def __init__(self):
    '''定义常用的期货相关的代码集。
    max28Codes=成交最活跃的前28名的wind商品指数代码；'''

#活跃合约代码list
    self.allActive=['I.DCE', 'WH.CZC', 'NI.SHF', 'SM.CZC', 'OI.CZC', 'PB.SHF',\
 'V.DCE', 'J.DCE', 'PM.CZC', 'FB.DCE', 'LR.CZC', 'RB.SHF', 'ZC.CZC', 'PP.DCE',\
 'P.DCE', 'AG.SHF', 'C.DCE', 'FG.CZC', 'A.DCE', 'RM.CZC', 'WR.SHF', 'TA.CZC',\
 'JR.CZC', 'ZN.SHF', 'HC.SHF', 'CU.SHF', 'JM.DCE', 'FU.SHF', 'B.DCE', 'MA.CZC',\
 'RI.CZC', 'M.DCE', 'SN.SHF', 'BB.DCE', 'CF.CZC', 'JD.DCE', 'AL.SHF', 'RU.SHF',\
 'RS.CZC', 'SF.CZC', 'AU.SHF', 'L.DCE', 'BU.SHF', 'Y.DCE', 'SR.CZC', 'CS.DCE']
#成交最大的wind商品指数代码
    self.max28=['RBFI.WI','MFI.WI', 'RMFI.WI', 'SRFI.WI', 'IFI.WI', \
'BUFI.WI', 'TAFI.WI', 'CFFI.WI', 'LFI.WI', 'MEFI.WI', 'PFI.WI', 'PPFI.WI',\
'RUFI.WI', 'FGFI.WI', 'CFI.WI', 'NIFI.WI', 'AGFI.WI', 'YFI.WI', 'CUFI.WI',\
'ZNFI.WI', 'CSFI.WI', 'TCFI.WI', 'HCFI.WI', 'AUFI.WI', 'ALFI.WI', 'AFI.WI',\
'OIFI.WI', 'JFI.WI']

#成交最大的wind商品所对应的活跃合约代码
    self.max28Active=['RB.SHF','M.DCE', 'RM.CZC', 'SR.CZC', 'I.DCE', 'BU.SHF',\
'TA.CZC', 'CF.CZC', 'L.DCE', 'ME.CZC', 'P.DCE', 'PP.DCE','RU.SHF', 'FG.CZC', \
'C.DCE', 'NI.SHF', 'AG.SHF', 'Y.DCE', 'CU.SHF','ZN.SHF', 'CS.DCE', 'TC.CZC', \
'HC.SHF', 'AU.SHF', 'AL.SHF', 'A.DCE','OI.CZC', 'J.DCE']

  def code(self):

    '获取客户输入的单一windcode'

    self.code=input('Please input a code:')
    return self.code


  def multiCodes(self):

    '逐一获取客户输入的edb代码，并合为一个字符串，用于通过wind python接口提取数据'

    codes=[]
    c='s5707135'
    while True:
        edb_code=input(r"windcode:")
        if edb_code != "":
        #edb_code='s'+ edb_code,有些指标s或m都有指标（m0175593，sm0175593)，容易混淆，所以输入全部，不能只输入数字
            codes.append(edb_code)
        else:
            break
    self.codes=','.join(codes)
    return c if len(self.codes) ==0 else self.codes


  def edbCodesFromClipboard(self):

    '''
    通过剪切板获得用户复制到剪切板上的edb代码，利用这些代码来调用接品获取数据
    '''
    d=self.dataFromClipboard()
  #  wc.OpenClipboard()
  #  d = wc.GetClipboardData(win32con.CF_TEXT)
  #  wc.CloseClipboard()
    self.codes=re.findall('[SMsm]+\d{7}',str(d))
    return self.codes

  def codesFromClipboard(self):

    '利用正则表达式获取客户剪切板中的多个代码'

    d=self.dataFromClipboard()
    self.codes=re.findall('[A-Za-z]{1,2}\d{,4}\.[A-Za-z]{3,4}',str(d))
    return self.codes

  def dataFromClipboard(self):
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    self.data=w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return self.data


  def dataToClipboard(self,aString):
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()
    return aString

  def windIndexCodesFromClipboard(self):
    '利用正则表达式获取客户剪切板中的多个代码（wind品种指数,如CUFI.WI）'
    d=self.dataFromClipboard()
    self.codes=re.findall('[A-Za-z]{3,4}\.WI',str(d))
    return self.codes

  def getActivecodes(self):

    '具体合约代码转活跃合约代码,如cu1609.shf转为cu.shf'
    rawcodes=str(self.codesFromClipboard())
    s=re.sub('\d{3,4}','',rawcodes)
    self.codes=self.dataToClipboard(s)
    self.codes=self.codesFromClipboard()
    return self.codes



def dateToString(date):
  '将日期转化为字符串'
  return str(date)[0:10]

class windDate():

#  def __init__(self):
#    self.today=datetime.date.today()
#    self.days=5

  def getYesterday(self,days=1):
    '取得昨天的日期'
    today=datetime.date.today()
    oneday=datetime.timedelta(days)
    self.yesterday=dateToString(today-oneday)
    return self.yesterday

  def getDaysByNum(self,num):
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    self.dayslist=[]
    for i in range(0,num):
        #今天减一天，一天一天减
        today=today-oneday
        #把日期转换成字符串
        #result=datetostr(today)
        self.dayslist.append(dateToString(today))
    return self.dayslist

#  def start(self,days=5):
#    return self.getYesterday(5)
#
#  def end(self):
#    return self.today
#
#  def tdays(self,start=start(5),end=end(),days=""):
#    days="days=%s" % days
#    temp=w.tdays(start, end, days)
#    return temp
#
##todo待完成
#
#
#
#
#
#
#
