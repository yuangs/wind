import pandas as pd
import requests
import re
import string
import time

dict_99={'99qh品种代码': {'AP': 100,
  'CF': 23,
  'FG': 72,
  'IC': 97,
  'IF': 63,
  'IH': 96,
  'MA': 89,
  'OI': 71,
  'RM': 74,
  'SF': 90,
  'SM': 91,
  'SR': 51,
  'T': 95,
  'TA': 53,
  'TF': 76,
  'ZC': 98,
  'a': 11,
  'ag': 69,
  'al': 7,
  'au': 58,
  'b': 12,
  'bu': 78,
  'c': 24,
  'cs': 92,
  'cu': 6,
  'hc': 85,
  'i': 79,
  'j': 65,
  'jd': 80,
  'jm': 75,
  'l': 56,
  'm': 16,
  'ni': 94,
  'p': 57,
  'pb': 64,
  'pp': 84,
  'rb': 59,
  'ru': 8,
  'sn': 93,
  'v': 61,
  'y': 52,
  'zn': 54},
 '品种': {'AP': '苹果',
  'CF': '一号棉',
  'FG': '玻璃',
  'IC': '中证五零零',
  'IF': '沪深三零零',
  'IH': '上证五零',
  'MA': '甲醇MA',
  'OI': '菜籽油',
  'RM': '菜籽粕',
  'SF': '硅铁',
  'SM': '锰硅',
  'SR': '白糖',
  'T': '十年期国债',
  'TA': 'PTA',
  'TF': '五年期国债',
  'ZC': '动力煤',
  'a': '豆一',
  'ag': '白银',
  'al': '铝',
  'au': '黄金',
  'b': '豆二',
  'bu': '石油沥青',
  'c': '玉米',
  'cs': '玉米淀粉',
  'cu': '铜',
  'hc': '热轧卷板',
  'i': '铁矿石',
  'j': '焦炭',
  'jd': '鸡蛋',
  'jm': '焦煤',
  'l': '聚乙烯',
  'm': '豆粕',
  'ni': '镍',
  'p': '棕榈油',
  'pb': '铅',
  'pp': '聚丙烯',
  'rb': '螺纹钢',
  'ru': '橡胶',
  'sn': '锡',
  'v': '聚氯乙烯',
  'y': '豆油',
  'zn': '锌'}}
var_list=list(dict_99['99qh品种代码'].keys())

def get_position_contract(date="2018-07-10",goods='cu'):
    code_99qh=dict_99['99qh品种代码'][goods]
    url='http://service.99qh.com/hold2/MemberHold/GetAgreementInfo.aspx?date=%s&goodsid=%s'%(date,code_99qh)
    df=requests.get(url)
    time.sleep(0.25)
#     print(url)
    return re.findall('<AgreementCode>(.*?)</AgreementCode>',df.text)


#获取某一日期所有有公布持仓的合约列表
def get_all_contracts(date):
    contracts=[]
    for commodity in var_list:
        contracts+=get_position_contract(date,commodity)
#         print(str(commodity)+str(contracts))
    return contracts

def get_oi(date="2018-07-10",goods=6,contract='cu1809',count=20):
    url=r'http://service.99qh.com/hold2/MemberHold/GetTableHtml.aspx?\
date=%s&user=99qh&goods=%s&agreement=%s&count=%s'%(date,goods,contract,count)
#     print(url)
    df=pd.read_html(url)
#      print(data)
    return df
    

def getData(data):
    df=data[0].iloc[2:,]
    df['v']=df.iloc[1,2]
    df['l']=df.iloc[1,6]
    df['s']=df.iloc[1,10]
    df['vr']=df.iloc[0,0]
    df['lr']=df.iloc[0,1]
    df['sr']=df.iloc[0,2]
    a=df[2:]
    va=pd.DataFrame(a.loc[:,[0,1,2,3,'v','vr']])
    la=pd.DataFrame(a.loc[:,[4,5,6,7,'l','lr']])
    sa=pd.DataFrame(a.loc[:,[8,9,10,11,'s','sr']])
    va.columns=la.columns=sa.columns=['Rank','Member','Value','Change','Index','Rank_type']
    aa=pd.concat([va,la,sa])
    df=data[2]
    df['v']=df.iloc[1,2]
    df['l']=df.iloc[1,6]
    df['s']=df.iloc[1,10]
    df['vr']=df.iloc[0,0]
    df['lr']=df.iloc[0,1]
    df['sr']=df.iloc[0,2]
    b=df[2:]
    vb=pd.DataFrame(b.loc[:,[0,1,2,3,'v','vr']])
    lb=pd.DataFrame(b.loc[:,[4,5,6,7,'l','lr']])
    sb=pd.DataFrame(b.loc[:,[8,9,10,11,'s','sr']])
    vb.columns=lb.columns=sb.columns=['Rank','Member','Value','Change','Index','Rank_type']
    bb=pd.concat([vb,lb,sb])
    df=data[3]
    df['v']=df.iloc[1,2]
    df['l']=df.iloc[1,6]
    df['s']=df.iloc[1,10]
    df['vr']=df.iloc[0,0]
    df['lr']=df.iloc[0,1]
    df['sr']=df.iloc[0,2]
    c=df[2:]
    vc=pd.DataFrame(c.loc[:,[0,1,2,3,'v','vr']])
    lc=pd.DataFrame(c.loc[:,[4,5,6,7,'l','lr']])
    sc=pd.DataFrame(c.loc[:,[8,9,10,11,'s','sr']])
    vc.columns=lc.columns=sc.columns=['Rank','Member','Value','Change','Index','Rank_type']
    cc=pd.concat([vc,lc,sc])
    data=pd.concat([aa,bb,cc],ignore_index=True)
    return data

def get_OIData(date="2018-07-02"):
    contracts=get_all_contracts(date)
    Data=pd.DataFrame()
    for contract in contracts:
        start=time.time()
        data1=pd.DataFrame()
        commodity=contract.rstrip(string.digits)
        goods=dict_99['99qh品种代码'][commodity]
        data=get_oi(date=date,goods=goods,contract=contract,count=20)
        data=getData(data)
        data['Date']=date
        data['Commodity']=commodity
        data['Contract']=contract
        data1=pd.concat([data1,data],ignore_index=True)
#         Dataj=pd.DataFrame()
        Data=pd.concat([Data,data1],ignore_index=True)
        time.sleep(0.1)
        end=time.time()
        print("合约%s的数据获取时间为："% contract +str(end-start))
    Data.to_csv('Daily_oi_%s.csv'% date)
    return Data

if __name__ == '__main__':
    get_OIData()
