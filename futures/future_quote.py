import pandas as pd
import numpy as np
import re
import json
import requests

def future_quote_sina():
    '获取新浪期货全部合约即时行情数据'
    r=requests.get('http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22qhhq%22,%22qbhy%22,%22zdf%22,1000]]')
    data=r.text
    data = json.loads(data)
    d=data[0]
    df=pd.DataFrame(d['items'],columns=d['fields'])
    df.head()
    df.index=df.name
    #交易所主力合约：df[(df.market=='dce')& (df.is_hot=='1')]
    #全部主力合约：df[(df.market=='dce')& (df.is_hot=='1')]
    #交易所合约：df[(df.market=='dce')]
    return df
future_quote_sina()

def future_quote_sina(code='by'):
    r=requests.get('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?\
    page=1&num=20&sort=position&asc=0&node=%s_qh&base=futures#'% code)
    text=r.text
    df=pd.DataFrame(np.array(re.findall('[a-z]+?:"(\w+?)"',text)).reshape(-1,18))
    columns=['symbol', 'market', 'contract', 'name', 'trade', 'settlement', 'prevsettlement', 'open', 'high', 'low',
     'close', 'bid', 'ask', 'bidvol', 'askvol', 'volume', 'position', 'currentvol']
    df.columns=columns
    df.index=df.symbol
    return df

def sc(code='lv',contract='al1705',which='trade'):
    contract=contract.upper()
    return future_quote_sina(code).loc[contract,which]

future_quote_sina('lv')
sc(code='lv',which='high')

pz={'bl': '玻璃',
 'bohai': '现货商品',
 'bst': '白糖',
 'by': '白银',
 'czp': '菜粕',
 'czy': '菜油',
 'dd': '豆一',
 'de': '豆二',
 'dlm': '动力煤',
 'dp': '豆粕',
 'dy': '豆油',
 'gt': '硅铁',
 'gz': '5年期国债期货',
 'hj': '黄金',
 'hym': '玉米',
 'jbx': 'PP',
 'jd': '鸡蛋',
 'jdm': '粳稻',
 'jhb': '胶合板',
 'jm': '焦煤',
 'jt': '焦炭',
 'lldpe': '塑料',
 'lq': '沥青',
 'lv': '沪铝',
 'lwg': '螺纹钢',
 'mg': '锰硅',
 'mh': '棉花',
 'ni': '沪镍',
 'pta': 'PTA',
 'pvc': 'PVC',
 'qian': '沪铅',
 'qm': '强麦',
 'qz': '沪深300指数期货',
 'ry': '燃油',
 'rzjb': '热轧卷板',
 'sngz': '10年期国债期货',
 'szgz': '上证50指数期货',
 'tks': '铁矿石',
 'tong': '沪铜',
 'wxd': '晚籼稻',
 'xc': '线材',
 'xi': '沪锡',
 'xing': '沪锌',
 'xj': '橡胶',
 'xwb': '纤维板',
 'ycz': '菜籽',
 'ymdf': '玉米淀粉',
 'zc': '郑醇',
 'zly': '棕榈',
 'zxd': '早籼稻',
 'zzgz': '中证500指数期货'}