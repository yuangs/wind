# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:33:01 2016
本脚本的作用是直接从大商网站上获取龙虎榜的持仓数据，交易所每日会生成一个持仓数据的文件，类似于：
http://www.shfe.com.cn/data/dailydata/kx/pm20160725.dat
直接pandas读取（pd.read_json）之后处理一下，生成所需要的dataframe;
@author: gsyuan
"""
import pandas as pd
import datetime
# 终于找到大商所的持仓下载链接了!
# http://www.dce.com.cn/PublicWeb/DPL_ZIP/2016084_DCE_DPL.zip
