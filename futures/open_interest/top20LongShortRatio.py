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

def LS_strenth(startdate=20161027,enddate=20161227,varity='RB.SHF',which='前二十名合计'):
    st=startdate
    ed=enddate
    vt=varity.upper()
    s=which
    d=w.wset("futureoir","startdate=%s;enddate=%s;varity=%s;order_by=long;ranks=all"%(st,ed,vt))
    df=pd.DataFrame(d.Data).T
    df.columns=d.Fields
    df.index=df.date
    df.dropna()
    df['ratio']=df[df.member_name=='%s'%s]['long_position']/df[df.member_name=='%s'%s]['short_position']
    #df['ratio_base']=df['ratio']/df['ratio'][-1]
    df['based_settle']=df['ratio'][-1]*df['settle']/df['settle'][-1]
    df['base']=1
    result=df[df.member_name==s][['member_name','settle','ratio','based_settle','base']].sort_index(ascending=True).head()
    df[df.member_name==s][['based_settle','ratio','base']].plot(figsize=(11,6))
    return (vt,result)
  
    LS_strenth(20151220,20161115,'j.dce','永安期货')
    
'''  ('J.DCE',
                         member_name settle     ratio based_settle  base
 date                                                                   
 2015-12-21 00:00:00.005        永安期货  636.5  0.273511     0.273511     1
 2015-12-22 00:00:00.005        永安期货  635.5  0.230837     0.273082     1
 2015-12-23 00:00:00.005        永安期货    635  0.225971     0.272867     1
 2015-12-24 00:00:00.005        永安期货  633.5  0.230158     0.272222     1
 2015-12-25 00:00:00.005        永安期货  629.5   0.20192     0.270503     1)'''
