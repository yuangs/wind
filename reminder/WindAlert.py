# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:31:50 2016

@author: gsyuan
"""
from WindPy import *
from constants import cons
from tools import getCode
from email.mime.text import MIMEText
from email.header import Header
import smtplib
w.start()

TRADEUNIT = cons.TRADEUNIT

CODES = list(TRADEUNIT.keys())


codes = getCode.windCode()
# print(codes)


def totalAmount(codes, baseDate='20160706', backwardDays=0):
    tradeTotal = 0
    baseDate = baseDate
    backDays = backwardDays
    backwardDays = 'ED-' + str(backwardDays) + "TD"
    for code in codes:
        data = w.wsd(code, "open,high,low,close,volume,oi,pct_chg", backwardDays,
                     baseDate)
        dt = data.Data
        for i in range(backDays + 1):
            date = data.Times[i]
            o = dt[0][i]
            h = dt[1][i]
            l = dt[2][i]
            c = dt[3][i]
            v = dt[4][i]
    #   pchg=data[5][0]
            avg = (o + h + l + c) / 4
            tradeAmount = v * avg * float(TRADEUNIT[code])
            print(str(date.strftime("%Y-%m-%d")) + ":" +
                  code + "的名义成交金额为:", tradeAmount / 10000)
            tradeTotal += tradeAmount
    return '名义成交量：' + str(tradeTotal / 10000) + "（万元）"


def alert(chg=3.1):
    '定义警示函数，扫描所有品种的涨幅幅，若超过某个限定的阈值，则发送邮件提醒自己注意！'
    codes = getCode.getActivecodes()
    dic = {}
    for code in codes:
        data = w.wsd(code, "close,pct_chg,oi,oi_chg", "ED-0TD").Data
        price = data[0][0]
        price_chg = data[1][0]
        if price:
            if price_chg > chg:
                dic[code] = [price, price_chg]
            else:
                pass
        else:
            print('没有有效的返回数据!')
    return dic


def vpup():
    '提取持仓与价格变动超过一定幅度的期货合作信息'
    codes = getCode.getCodes()
    dic = {}
    for code in codes:
        data = w.wsd(code, "close,pct_chg,oi,oi_chg", "ED-1TD").Data
        if isinstance((data[1][-1]), float):
            price = data[0][-1]
            price_chg = data[1][-1]
            oi = data[2][-1]
            oi_chg = data[3][-1]
        else:
            price = data[0][-2]
            price_chg = data[1][-2]
            oi = data[2][-2]
            oi_chg = data[3][-2]
        if oi != 0:
            oichg = oi_chg / oi
        else:
            oichg = 0
        if abs(oichg) > 0.05 and abs(price_chg) > 1.5:
            dic[code] = ' '.join(['Oichg:%.2f%%' % (100 * oichg), 'Oi:%.0f' % oi,
                                  'Pricechg:%.2f%%' % price_chg, 'Price:%.0f' % price])
        else:
            pass
    return dic


def sendMail(message):
    '定义发送邮件函数，用以发送警示信息'

    sender = 'gsyuan@wind.com.cn'
    receiver = '516309388@qq.com'
    subject = 'python email test'
    smtpserver = 'shms3.wind.com.cn'
    username = 'gsyuan'
    password = '******'
    username = 'yuanguangshan'
    password = '******'

    msg = MIMEText(message, 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def hashvalue():
    from hashlib import md5

    str = input('input str to hash:')
    m = md5()
    m.update(str.encode('utf8'))
    print(m.hexdigest())


if __name__=="__main__":
    print(TRADEUNIT)
    # print(totalAmount(codes))
    # sendMail(message)

