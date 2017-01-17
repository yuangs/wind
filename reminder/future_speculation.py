# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:46:00 2016

@author: gsyuan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from WindPy import *

w.start()  #
#计算所有期货品种的投机度，并绘制出图表方便观察各品种的热门程度
def hot():
  date='20161021'
  #获取上述默认日期所有期货品种的成交量及持仓量的数据
  field="A.DCE,AG.SHF,AL.SHF,AU.SHF,B.DCE,BB.DCE,BU.SHF,C.DCE,CF.CZC,CS.DCE,CU.SHF,FB.DCE,FG.CZC,FU.SHF,HC.SHF,I.DCE,J.DCE,JD.DCE,JM.DCE,JR.CZC,L.DCE,LR.CZC,M.DCE,MA.CZC,NI.SHF,OI.CZC,P.DCE,PB.SHF,PM.CZC,PP.DCE,RB.SHF,RI.CZC,RM.CZC,RS.CZC,RU.SHF,SF.CZC,SM.CZC,SN.SHF,SR.CZC,TA.CZC,TC.CZC,V.DCE,WH.CZC,Y.DCE,ZC.CZC,ZN.SHF,WR.SHF,AG(T+D).SGE,AU(T+D).SGE"
  index="oi,volume"
  date="tradeDate=%s;priceAdj=U;cycle=D" % date
  codes=oi=w.wss(field,index,date).Codes
  oi=w.wss(field,index,date).Data[0]
  volume=w.wss(field,index,date).Data[1]

  #将列获取的数据转化为numpy对象
  oi=pd.Series(oi,index=codes)
  volume=pd.Series(volume,index=codes)

  #计算投机度
  touji=volume/oi

  #删除数据列中的空值，以备图表和数据输出之用
  hot=touji.dropna()
  hot.columns='hot'
  #打印出热度最高的十个品种
  print('[%s]\n投机度最高的前十名为：' % date)
  print(hot.nlargest(10))
  #打印出热度最低的十个品种
  print('[%s]\n投机度最低的前十名为：' % date)
  print(hot[hot!=0].nsmallest(10))
  #排除空值
  hot[hot!=0].plot(kind='bar',figsize=(10.5, 4.2))

def getchart():
  '读取剪切板的期货或股票的历史导出数据，输出均价、成交量、持仓量等信息'
  read=pd.read_clipboard(header=0,index_col=0)
  #转化为pandas的timeindex格式，方便对数据重新取样
  index=pd.to_datetime(read.index)
  #处理labels和llabel's name
  read.index=index
  read.index.name=""

  if len(read.columns)==8:
    '''对期货（主力合约和具体合约）都具有八列，如铁矿石I.DCE：
    日期	开盘价(元)	最高价(元)	最低价(元)	收盘价(元)	结算价	成交额(百万)	成交量	持仓量
    2016-03-15	419.5	428	410.5	413	419.5	203805.42	4856536	1039788
    2016-03-16	410.5	421	410	419	415.5	138065.06	3321042	1061572
    2016-03-17	420.5	436.5	416	435.5	426	188942.64	4432586	1086568
    2016-03-18	435.5	451.5	433.5	449.5	445	175160.16	3934660	933232
    2016-03-21	414	431	410	422.5	423.5	208160.62	4910998	1231352
    '''
    read['投机度']=read.成交量/read.持仓量
    read['投机度'].plot()
    sample=read.resample('3M').mean().iloc[:,[-1,-5,-4,-2]]
    sample.plot(subplots=True, layout=(2, 2), figsize=(10, 6), sharex=False);
  else:
    '''
    对股票来说，只有六列，如同仁堂（6000085）
    日期	开盘价(元)	最高价(元)	最低价(元)	收盘价(元)	成交额(百万)	成交量
    2016-04-14	29.95	30	29.69	29.88	270.52	9072700
    2016-04-15	29.97	30	29.75	29.83	190.35	6381000
    2016-04-18	29.8	29.81	29.18	29.2	228.48	7785300
    2016-04-19	29.31	29.43	28.91	29.1	161.17	5541900
    2016-04-20	29.15	29.28	27.11	28.4	391.68	13885100
    '''
    read['成交均价']=read['成交额(百万)']/read['成交量']
    sample=read.resample('3M').mean().iloc[:,[-1,-4,-3,-2]]
    sample.plot(subplots=True, layout=(2, 2), figsize=(10, 6), sharex=False)


hot()
getchart()








