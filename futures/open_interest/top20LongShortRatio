import pandas as pd
from WindPy import *
w.start()

def longShortRatio(pz,sj,hy=''):
    if hy!="":
        query="startdate=%s;enddate=%s;varity=%s;wind_code=%s;order_by=long;ranks=all" %(sj,sj,pz.upper(),hy.upper())
        print('%s多空对比统计：'% hy)
    else:
        query="startdate=%s;enddate=%s;varity=%s;order_by=long;ranks=all" %(sj,sj,pz.upper())
        print('%s多空对比统计：'% pz)
    d=w.wset("futureoir",query)
    df=pd.DataFrame(d.Data).T
    df.columns=d.Fields
    df.index=df.member_name
    r5=df[df.member_name=='前五名合计']['long_position']/df[df.member_name=='前五名合计']['short_position']
    r10=df[df.member_name=='前十名合计']['long_position']/df[df.member_name=='前十名合计']['short_position']
    r20=df[df.member_name=='前二十名合计']['long_position']/df[df.member_name=='前二十名合计']['short_position']
   # print('%s多空对比统计：'% pz)
    print('前五名多空比为：%.2f%%' %(r5.values[0]*100))
    print('前十名多空比为：%.2f%%' %(r10.values[0]*100))
    print('前二十名多空比为：%.2f%%' %(r20.values[0]*100))
    
longShortRatio('rb.shf',20161226,'rb1705.shf')

'''

rb1705.shf多空对比统计：
前五名多空比为：93.59%
前十名多空比为：102.26%
前二十名多空比为：98.77%
'''
