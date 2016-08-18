# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:33:01 2016
本脚本的作用是直接从上期所网站上获取龙虎榜的持仓数据，交易所每日会生成一个持仓数据的文件，类似于：
http://www.shfe.com.cn/data/dailydata/kx/pm20160725.dat
直接pandas读取（pd.read_json）之后处理一下，生成所需要的dataframe;
@author: gsyuan
"""
import pandas as pd

oi=pd.DataFrame(pd.read_json('http://www.shfe.com.cn/data/dailydata/kx/pm20160725.dat'))
index=oi.index
lis=[]
for i in range(len(index)):
  f=oi.o_cursor[i]
  raw={
  '合约':f['INSTRUMENTID'],
  '名次':f['RANK'],
  '期货公司会员简称':f['PARTICIPANTABBR1'],
  '成交量':f['CJ1'],
  '成交较上日增减':f['CJ1_CHG'],
  '期货公司会员简称2':f['PARTICIPANTABBR2'],
  '多单量':f['CJ2'],
  '多单较上日增减':f['CJ2_CHG'],
  '期货公司会员简称3':f['PARTICIPANTABBR3'],
  '空单量':f['CJ3'],
  '空单较上日增减':f['CJ3_CHG']
  }
  lis.append(raw)
df=pd.DataFrame(lis,index=index)
result=df.iloc[:,[0,1,6,5,4,7,3,2,8,10,9]]
print(result)
