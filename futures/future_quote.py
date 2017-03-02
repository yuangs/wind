import pandas as pd
import numpy as np
import re
import json
import requests


def future_quote_sina(exchange='all', flag=1):
    '''获取新浪期货全部合约即时行情数据,默认取全部交易所主力合约，取特定交易所主力或全部合约，用参数来指定
    para:
        exchange:   all,shfe,dce,czce
        flag:       1（active contracts),0(non-active contracts),2(all contracts)
    result:
        dataframe
    '''
    r = requests.get(
        'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22qhhq%22,%22qbhy%22,%22zdf%22,1000]]')
    data = r.text
    data = json.loads(data)
    d = data[0]
    df = pd.DataFrame(d['items'], columns=d['fields'])
    df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))  #
    df.index = df.name
    # 交易所主力合约：df[(df.market=='dce')& (df.is_hot=='1')]
    # 全部主力合约：df[(df.market=='dce')& (df.is_hot=='1')]
    # 交易所合约：df[(df.market=='dce')]
    if exchange == 'all':
        if flag != 2:
            # 三大交易所主力（非主力）合约
            return df[df.is_hot == flag].sort_values('volume', ascending=False)
        else:
            # 三大交易所全部合约
            return df.sort_values('volume', ascending=False)
    else:
        if flag != 2:
            # 指定交易所主力（非主力）合约
            return df[(df.market == exchange) & (df.is_hot == flag)].sort_values('volume', ascending=False)
        else:
            # 指定交易所全部合约
            return df[df.market == exchange].sort_values('volume', ascending=False)

def future_overseas_sina():
    '获取新浪期货外盘期货的即时行情数据'
    r = requests.get('http://vip.stock.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22wpqh%22,%22spqh%22]]')
    data = r.text
    data = json.loads(data)[0]
    df=pd.DataFrame(data['items'],columns=data['fields'])
    df.index=df.symbol
    columns=['name','dateupdate','timeupdate', 'last', 'changeamount', 'pricechange','totalvol',\
         'bid', 'ask','prev', 'open', 'high', 'low']
    data=df.loc[:,columns]
    return data


if __name__=='__main__':
    import time
    while True:
        a=future_quote_sina('all', 1)
        print(a.loc['铁矿石1705',['name', 'trade','volume', 'position']])
        #print(a.columns)
        print('小猪猪，数据提取完毕!!!!')
        time.sleep(1)
    