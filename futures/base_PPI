# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:09:19 2017
获取生意社期现表数据，这里有现货价格，期货价格以及现货与近月，主力合约的基差，基差率等信息。
@author: Administrator
"""


import pandas as pd
import datetime

date=datetime.datetime.now()
year=date.year
month=date.month
day=date.day

url='http://www.100ppi.com/sf/day-{0}-{1}-{2}.html'.format(year,month,day-1)
data=pd.read_html(url)[1].dropna()
columns=['商品','现货价','近月合约','近月价格','a','近月基差','近月基差（%）','主力合约','主力价格','b','主力基差','主力基差（%）']
data.columns=columns
data.index=data.商品
del data['商品']
del data['a']
del data['b']
print(data)
