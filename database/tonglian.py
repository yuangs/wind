import pandas as pd
import datetime as dt
import pprint
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
pp=pprint.PrettyPrinter(indent=4)


def tongLian(indicId=2020100024,start=20100101,end=20171231):
    '获取通联数据的接口，指数代码名称以及起始日期'
    url='https://gw.wmcloud.com/rrp/mobile/whitelist/data?indicID=%s&beginDate=%s&endDate=%s'%(indicId,start,end)
    print(url)
    f=pd.read_json(url)
    # pp.pprint(f[1:-1].dataDetailNewList.to_dict())
    name=f.loc['name','dataDetailNewList']
    data=pd.DataFrame(f.loc['dataDetail','dataDetailNewList'])
    data.columns=[name,'date']
    data.index=data.date.map(lambda x: dt.datetime.fromtimestamp(x/1000))
    del data['date']
    data.sort_index(inplace=True)
    return data


def clip2dict():
    '复制指数名称和代码到剪切板中，转化为dict,供给batch_data使用'
    clipboard=pd.read_clipboard(header=None)
    d=clipboard.to_dict( orient='index')
    data={d[i][0]:d[i][1] for i in range(len(d))}
    return data


def batch_data(code):
    '批量获取通联数据，不过先要把指标名称及id复制到剪切板中'
    ls=list(code.keys())
    data={i:tongLian(code[i]) for i in ls}
    df=pd.concat([data[i] for i in ls],axis=1)
    df.dropna(thresh=2)
    return df


if __name__ == '__main__':
	batch_data=batch_data(clip2dict())
	print(batch_data)

