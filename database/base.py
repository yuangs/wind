#!/usr/bin/python3

import pandas as pd
import datetime

date=datetime.datetime.now()
year=date.year
month=date.month
day=date.day

def base(day=day-1):
	url='http://www.100ppi.com/sf/day-{0}-{1}-{2}.html'.format(year,month,day)
	data=pd.read_html(url)[1].dropna()
	columns=['商品','现货价','近月合约','近月价格','a','近月基差','近月基差（%）','主力合约','主力价格','b','主力基差','主力基差（%）']
	data.columns=columns
	data.index=data.商品
	data['date']='%s-%s-%s'%(year,month,day)
	del data['商品']
	del data['a']
	del data['b']
	#print(data.head(1))
	return data#.to_html('./static/base.html')


def futures(day=day-1):
	d=pd.read_html(r'http://futures.100ppi.com/')
	data=pd.concat(list(d[i] for i in range(1,len(d)-1) ), ignore_index=True)
	data.iloc[12,-1]='shf';data.iloc[29,-1]='czce';data.iloc[46,-1]='dce';data.iloc[59,-1]='cme';data.iloc[72,-1]='cbot';data.iloc[83,-1]='nymex';\
	data.iloc[90,-1]='comex';data.iloc[107,-1]='ice_europe';data.iloc[114,-1]='ice_us';data.iloc[119,-1]='ice_canada';data.iloc[133,-1]='tocom';\
	data.iloc[136,-1]='sgx';data.iloc[171,-1]='mcx';data.iloc[179,-1]='dubai'
	data.iloc[:,-1]=data.iloc[:,-1].fillna(method='bfill')
	data.fillna("").iloc[1:,:]
	data.columns=["商品名称","主力合约","前结算","今开盘","最高价","最低价","收盘价","结算价","涨跌2","成交量","持仓量","持仓量变化",\
	              "报价单位","交易所"]
	data.drop_duplicates(["商品名称","主力合约","成交量"],inplace=True)
	df=data.iloc[1:,:].fillna("")
	df.set_index('商品名称',inplace=True)
	df['成交量']=pd.to_numeric(df['成交量'],errors='coerce')
	df.sort_values('成交量',ascending=False,inplace=True)
	#print(df.head(1))
	return df#.to_html('./static/futures.html')

def dailyPrice(day=day-1):
	a=base()
	b=futures()
	b.columns=['主力合约', '现货价', '主力基差', '近月价格', '近月基差', '收盘价', '时间', '涨跌2', '成交量', '持仓量',
	       '持仓量变化', '报价单位', '交易所']
	b['现货价']=a.现货价;b['主力基差']=a.主力基差;b['近月价格']=a.近月价格;b['近月基差']=a.近月基差;b['时间']=a.date;
	df=b.loc[:,['交易所','主力合约', '收盘价','现货价', '主力基差', '近月价格', '近月基差', '涨跌2', '成交量', '持仓量',
       '持仓量变化', '报价单位','时间',]]
	df.fillna("",inplace=True)
	print(df)   
	return df.to_html('./static/dailyPrice.html')

def dce_price(date='20170105'):
    url='http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html?dayQuotes.variety=all&dayQuotes.trade_type=0&year=%s&month=%s&day=%s'%(date[:4],int(date[4:6])+1,date[6:])
    html=pd.read_html(url)
    df=html[0]
    return df


if __name__ == '__main__':
	try:
		print(base())
		print(futures())
		print(dailyPrice(day=day))
	except:
		print(base(day-1))
		print(futures(day-1))
		print(dailyPrice(day=day-1))
	# df=pd.DataFrame()
	# for i in s[:100]:
	#     try:
	#         df=pd.concat([df,dce_price(i)],ignore_index=True)
	#         df['date']=i
	#         print(i)
	#     except:
	#         pass
	#     time.sleep(8)
	# print(df)

#to do 
#大宗58榜，生意社监控的58种大宗商品的价格涨跌情况。
