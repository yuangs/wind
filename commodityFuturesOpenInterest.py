# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 08:44:30 2016
利用wind python接口获取机构持仓数据，以供策略分析之用；
Using wind python interface to get hoding structure.
@author: 苑广山
@Email: yuanguangshan@163.com
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 07 13:52:32 2016

@author: gsyuan
"""
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np
import datetime,time

from WindPy import *
from pandas import Series,DataFrame

w.start()

def controlstr():
        cs={}
        cs['a']='startdate='+str(input(u'请输入开始日期(如，20160606):'))
        cs['b']='enddate='+str(input(u'请输入结束日期(如，20160606):'))
        cs['c']='varity='+str(input(u'请输入品种(如，rb.shf):'))
        cs['d']='wind_code=all'
        cs['e']='member_name=all'
        cs['f']='order_by='+str(input(u'请输入排序依据(long or short):'))
        L=list(cs.keys())
        L.sort()
        c=";".join([cs[k] for k in L])
        return c

c=controlstr()#构造关键字参数字符串
wd=w.wset("futureoi", c)#获取持仓数据，原始格式

def data_arrange(data=wd):
    columns=data.Data[0]#不包括日期列，这个用来做index
    columns=[i.strftime('%y%m%d') for i in columns]
    index=data.Fields[1:]
    data=data.Data[1:]
    return data,index,columns
    
d=data_arrange(data=wd)
'''
#获取wind持仓数据
#wind数据的格式:
#w.wset("futureoi","startdate=20150607;enddate=20160607;varity=al.shf;wind_code=all;\
#member_name=all;order_by=long")
'''
#c=controlstr()#构造关键字参数字符串
#wd=w.wset("futureoi", c)#获取持仓数据，原始格式
#data=data_arrange(data=wd)

dp=DataFrame(d[0],index=d[1],columns=d[2]).T

print(dp)
filenamestr=datetime.now().strftime('%y%m%d_%H%M%S')
dp.to_csv(r"C:\Users\gsyuan\Desktop\Wind Data\\"+filenamestr+".csv")
