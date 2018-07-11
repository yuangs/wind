import pandas as pd
import requests
import matplotlib.pyplot as plt  
import re
# %matplotlib inline

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
#     print(url)
    return re.findall('<AgreementCode>(.*?)</AgreementCode>',df.text)

def get_oi(date="2018-07-10",goods=6,contract='cu1809',count=20):
    url=r'http://service.99qh.com/hold2/MemberHold/GetTableHtml.aspx?\
date=%s&user=99qh&goods=%s&agreement=%s&count=%s'%(date,goods,contract,count)
    print(url)
    df=pd.read_html(url)
    data=pd.concat([df[0],df[2],df[3]]).iloc[2:,1:]
    print(data)
    return data

for i in var_list:
    con_list=get_position_contract(goods=i)
    for j in con_list:
        data=get_oi(date="2018-07-10",goods=dict_99['99qh品种代码'][i],contract=j,count=20)
        print(data)
