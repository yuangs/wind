#! _*_coding=utf-8_*_
import pandas as pd
import json
import requests
import time
from base import *

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
        if flag == 0:
            # flag=0,返回四大交易所非主力合约
            return df[df.is_hot == flag].sort_values('volume', ascending=False)
        elif flag==1:
            #flag=1,返回四大交易所主力合约
            return df[df.is_hot >= flag].sort_values('volume', ascending=False)
        elif flag==-1:
            # flag=-1,返回四大交易所全部合约
            return df.sort_values('volume', ascending=False)
    else:
            # 指定交易所主力（非主力）合约
        if flag == 0:
            #返回指定交易所非主力合约
            return df[(df.market == exchange) & (df.is_hot == flag)].sort_values('volume', ascending=False)
        elif flag == 1:
            #返回指定交易所非主力合约
            return df[(df.market == exchange) & (df.is_hot >= flag)].sort_values('volume', ascending=False)
        else:
            # 指定交易所全部合约
            return df[df.market == exchange].sort_values('volume', ascending=False)


def hot():
    a=future_quote_sina()
    a['hot']=a.volume/a.position
    a['current_time']=timenow()
    return a.loc[:,['trade','zdf','volume','position','hot','current_time']].to_html('/root/yuangs/www/my_flask/static/hot.html')

def hpl20(flag=0):
    f=future_quote_sina()
    h20=f.h_20t
    l20=f.l_20t
    price=f.trade
    f['hl']=100*(h20/l20-1)
    f['pl']=100*(price/l20-1)
    f.loc[:,['trade','zdf','volume','position','pl','hl']].to_html('/root/yuangs/www/my_flask/static/hpl.html')

def timenow():
    return time.asctime( time.localtime(time.time()) )

if __name__=='__main__':
    timenow()
    ppi_data()
    hot()
    hpl20(0)
    hpl20(1)


#add this line by sftp at 21:33 saturday


    
