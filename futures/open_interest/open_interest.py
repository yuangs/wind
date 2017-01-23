# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:33:01 2016

@author: gsyuan
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:33:01 2016

@author: gsyuan
"""
import pandas as pd
import numpy as np
import re
import requests
%matplotlib inline


def statistics(result):
    total = result.apply(np.sum)
    total.Name_1 = total.Name_2 = total.Name_3 = '总计'
    total.Code = ''
    total.Rank = ''

    statistics = total.tolist()
    result = result.append(pd.DataFrame(statistics, index=result.columns).T)
    result = result.apply(lambda x: pd.to_numeric(x, errors='ignore')).copy()
    return result


def shf_contract(code='cu', date=20170119):
    '''
    获取上期所某个合约某一交易日的持仓信息，解析为pandas dataframe
    上期所通过单一文件提供每日持仓龙虎榜数据的展示，通过解析json文件为字典，
    最后转化为pandas dateframe

    para:
    code:字符串，如'cu1705'
    date:八位日期格式，如20170117
    '''
    oi = pd.DataFrame(pd.read_json('http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat' % date))
    index = oi.index

    lis = []
    for i in range(len(index)):
        f = oi.o_cursor[i]
        raw = {
            '日期': date,
            '合约': f['INSTRUMENTID'],
            '名次': f['RANK'],
            '期货公司会员简称': f['PARTICIPANTABBR1'],
            '成交量': f['CJ1'],
            '成交较上日增减': f['CJ1_CHG'],
            '期货公司会员简称2': f['PARTICIPANTABBR2'],
            '多单量': f['CJ2'],
            '多单较上日增减': f['CJ2_CHG'],
            '期货公司会员简称3': f['PARTICIPANTABBR3'],
            '空单量': f['CJ3'],
            '空单较上日增减': f['CJ3_CHG']
        }
        lis.append(raw)

    df = pd.DataFrame(lis, index=index)
    result = df.loc[:, ['日期', '合约', '名次', '期货公司会员简称', '成交量', '成交较上日增减', '期货公司会员简称2', '多单量', '多单较上日增减',
                        '期货公司会员简称3', '空单量', '空单较上日增减']]
    result.columns = ['date', 'Code', 'Rank', 'Name_1', 'Volume', 'Vol_chg', 'Name_2', 'Long', 'Long_chg',
                      'Name_3', 'Short', 'Short_chg']
    result.set_index('date', inplace=True)
    '将可以转化为数字的列转换为数值类型'
    result = result.apply(lambda x: pd.to_numeric(x, errors='ignore')).copy()
    result = result[result.Code.str.contains(code)]
    selector = result['Rank'].apply(lambda x: x in list(range(1, 21)))
    result = result[selector]

    return statistics(result)


# 函数调用,
# shfe_contract('rb',20170119)
# shfe_contract('rb',20170119)

# 品种成交、多头，空头龙虎榜前二十名
def shf_variety(code='cu', date=20170119):
    '由于交易所不公布品种总持仓的排名情况，需求按各个合约汇总计算得出品种持仓龙虎榜数据'

    data = shf_contract(code, date)
    # 筛选出期公司的持仓记录，不包括统计记录，如期货公司，非期货公司，前二十名持仓汇总数据等。
    selector = data['Rank'].apply(lambda x: x in list(range(1, 21)))
    data = data[selector]
    # 按期货公司统计成交量加总，之后排序取前二十名
    df1 = pd.DataFrame(data.groupby('Name_1')['Name_1', 'Volume', 'Vol_chg'].sum() \
                       .sort_values('Volume', ascending=False).head(20))
    df2 = pd.DataFrame(data.groupby('Name_2')['Name_2', 'Long', 'Long_chg'].sum() \
                       .sort_values('Long', ascending=False).head(20))
    df3 = pd.DataFrame(data.groupby('Name_3')['Short', 'Short_chg'].sum() \
                       .sort_values('Short', ascending=False).head(20))

    # 重新索引以方便后续join操作
    df1.reset_index('rank', inplace=True)
    df2.reset_index('rank', inplace=True)
    df3.reset_index('rank', inplace=True)
    # 最终品种持仓龙虎榜
    df = df1.join(df2).join(df3)
    df['date'] = date
    df['Code'] = code
    df.set_index('date', inplace=True)
    columns = ['Code', 'Name_1', 'Volume', 'Vol_chg', 'Name_2', 'Long', 'Long_chg', 'Name_3',
               'Short', 'Short_chg']
    result = df.loc[:, columns]
    # 计算品种持仓的前十名统计数据
    return statistics(result)


def shf_oi(code='cu', date=20170119):
    '根据用户输入的参数选择提取品种或合约龙虎榜数据'
    if len(code) <= 2:
        return shf_variety(code, date)
    else:
        return shf_contract(code, date)


# 函数调用
oi_rank = shf_oi('cu1703', 20170119)
oi_rank


def dce_oi(code='i1705', date=20170119):
    '''
    获取大商所某个合约某一交易日的持仓信息，解析为pandas dataframe。

    大商所持仓信息网址格式如下：http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html?\
    memberDealPosiQuotes.variety=a&memberDealPosiQuotes.trade_type=0&year=2017&month=0&day=10&\
    contract.contract_id=all&contract.variety_id=a
    para:
    code:如果提取品种龙虎榜，参数只传字母代码，如i,a,取具体合约传代码全称，如i1705,a1705
    date:八位日期格式，如20170117
    '''
    date = str(date)
    if len(code) <= 2:
        variety = code
        contract = 'all'
    else:
        variety = code[:-4]
        contract = code

    url = 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html?\
memberDealPosiQuotes.variety=%s&memberDealPosiQuotes.trade_type=0&year=%s&month=%s&day=%s\
&contract.contract_id=%s' % (variety, date[:4], str(int(date[4:6]) - 1), date[6:], contract)

    s = pd.read_html(url, header=0, index_col=None, encoding='UTF-8')
    result = s[1].apply(lambda x: pd.to_numeric(x, errors='ignore')).copy()
    result['date'] = date
    result['code'] = code
    result.set_index('date', inplace=True)
    result.columns = ['Rank', 'Name_1', 'volume', 'Vol_chg', 'rank_2', 'Name_2', 'Long', 'Long_chg', \
 'rank_3', 'Name_3', 'Short', 'Short_chg', 'Code']
    result = result.loc[:, ['Code', 'Rank', 'Name_1', 'volume', 'Vol_chg', 'Name_2', 'Long', 'Long_chg', \
'Name_3', 'Short', 'Short_chg']]

    return statistics(result.head(20))


# 函数调用,
dce_oi('i', 20170119)
# dce_oi('i1705',20170119)

def czc(code='cf', date=20170117):
    code = code.upper()
    date = str(date)
    url = 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataHolding.htm' % (date[:4], date)
    data = pd.read_html(url, encoding='gb2312')[1].fillna(method='bfill')
    s = data[0]
    for i in range(len(s)):
        if '日期' in s[i]:
            s[i] = re.findall('[A-Z]{2,3}\d*', s[i])[0]
        elif '名次' in s[i]:
            s[i] = s[i - 1]
        else:
            s[i] = s[i - 1]
    data['日期'] = date
    data.set_index('日期', inplace=True)
    df = data.drop_duplicates()
    df.columns = ['Code', 'Name_1', 'volume', 'Vol_chg', 'Name_2', 'Long', 'Long_chg', \
                  'Name_3', 'Short', 'Short_chg']
    df = df.loc[:, ['Code', 'Rank', 'Name_1', 'volume', 'Vol_chg', 'Name_2', 'Long', 'Long_chg', \
                    'Name_3', 'Short', 'Short_chg']]
    result = df[df['Code'] == code][1:-1]
    result['Rank'] = list(range(1, 21))
    result = result.apply(lambda x: pd.to_numeric(x, errors='ignore')).copy()

    return statistics(result)

#函数调用
# czc('cf',20170119)
czc('cf705', 20170119)


def oi_99qh(code='rb', date=20170119, contract='ALL'):
    '99期货持仓数据接口'
    code2num = {'a': 78,
                'ag': 58,
                'al': 91,
                'au': 7,
                'bb': 79,
                'bu': 85,
                'c': 11,
                'cf': 23,
                'cs': 82,
                'cu': 89,
                'fb': 75,
                'fg': 70,
                'hc': 64,
                'i': 61,
                'j': 56,
                'jd': 65,
                'jm': 57,
                'l': 16,
                'ma': 94,
                'ni': 69,
                'p': 24,
                'pb': 54,
                'pp': 80,
                'rb': 8,
                'rm': 72,
                'rs': 71,
                'ru': 98,
                'sm': 74,
                'sr': 51,
                'ta': 53,
                'v': 52,
                'y': 12,
                'zn': 6}
    codenum = code2num[code]
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    url = 'http://service.99qh.com/hold2/MemberHold/GetTableHtml.aspx?date=%s-%s-%s&user=99qh&goods=%s&agreement=%s&count=20' % (
    year, month, day, codenum, contract)
    f = pd.read_html(url, encoding='utf-8')

    df = f[0][4:]
    df.columns = ['rank1', 'name', 'vol', 'vol_chg', 'rank2', 'name2', 'l', 'l_chg', 'rank3', 'name3', 's', 's_chg']
    df.to_clipboard()
    print('时间：%s  品种：%s  合约：%s 持仓情况' % (date, code, contract))
    print('数据来源：', url)
    return df


oi_99qh('rb', 20170120, 'rb1710')


def plot():
    def lsratio(code='rb', date=20170119, contract='ALL'):
        '计算前二十名多空比率'

        try:
            data = oi_99qh(code, 20170120)
            ratio = round(int(data.loc[24, 'l']) / int(data.loc[24, 's']), 2)
            return ratio
        except:
            pass


    def plot_data():
        '报价总是取最新交易时间'
        url = 'http://webftcn.hermes.hexun.com/shf/sortlist?block=741&number=100&title=14&commodityid=0&direction=0&start=0&column=code,name,price,updown,buyPrice,buyVolume,sellPrice,sellVolume,volume,lastClose,open,high,low,openInterest,addPosition,amount,vibrationRatio,priceWeight,dateTime&callback=hx_json11485071465878'
        r = requests.get(url)
        json = re.findall(r'\["(.*?)",".*?",(\d+),(\d+)', r.text)
        data = pd.DataFrame(json)
        data.columns = ['code', 'price', 'chg']
        data['code2'] = data.code.str.extract('([A-Z]+)')
        data = data.apply(lambda x: pd.to_numeric(x, errors='ignore')).copy()
        data['chg'] = data.chg / data.price
        data['ratio'] = data.code2.apply(lambda x: lsratio(x.lower()))
        df = data.dropna().copy()
        return df


    df = plot()
    df.plot(kind='scatter', x='chg', y='ratio')


