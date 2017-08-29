import pandas as pd
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

def rsi20():
    f=future_quote_sina()
    f['unit']=g.unit
    print(f.unit)
    print(f.columns)
    price=f.trade
    volume=f.volume
    position=f.position
    h20=f.h_20t
    l20=f.l_20t
    unit=g.unit
    f['t_amt']=price*volume*unit
    f['h_amt']=price*position*unit
    f['hot']=volume/position
    f['h20_from_l20']=100*(h20/l20-1)
    f['price_from_l20']=100*(price/l20-1)
    f['t_ratio']=f.t_amt/f.t_amt.sum()
    f['h_ratio']=f.h_amt/f.h_amt.sum()
    f.to_clipboard()
    
rsi20()


    
