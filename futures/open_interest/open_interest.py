# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:33:01 2016

@author: gsyuan
"""
import pandas as pd
import re


def shfe_oi(code='cu', date=20060106):
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

    return result[result.Code.str.contains(code)]


# 函数调用,
shfe_oi('rb1705', 20170117)
# 品种成交、多头，空头龙虎榜前二十名
# shfe_oi('cu',20170117).groupby('Name_1')['Volume','Vol_chg'].sum().sort_values('Volume',ascending=False).head(22)
# shfe_oi('cu',20170117).groupby('Name_2')['Long','Long_chg'].sum().sort_values('Long',ascending=False).head(22)
# shfe_oi('cu',20170117).groupby('Name_3')['Short' ,'Short_chg' ].sum().sort_values('Short',ascending=False).head(22)

def dce_oi(code='i1705', date=20170117):
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

    return result


# 函数调用,
dce_oi('a', 20170117)


def czc(code='cf705', date=20170117):
    '''
       获取郑商所某个合约某一交易日的持仓信息，解析为pandas dataframe
       para:
       code:字符串，如'cf705'或‘cf’
       date:八位日期格式，如20170117
       '''
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
    return df[df[0] == code]


czc()
