#-*- encoding: UTF-8 -*-
from lxml import html
import requests
import pandas as pd

def smm():
    '''获取smm的每日有色金属报价数据,e.g.
            name           price     aver change   date
    0        1#铜     36980-37150    37065   -105  08-16
    1        升贴水   (贴) 40-(升) 50        5    -95  11:30
    2   洋山铜溢价($)         $ 40-50     $ 45      0  08-16
    3     跨境人民币价   265.88-332.36   299.12  -0.16  08-16
    4       A00铝     12590-12630    12610     10  08-16
    5        升贴水  (升) 80-(升) 120      100    240  10:15
    6        1#铅     13650-13750    13700    -75  08-16'''
    url='http://www.smm.cn/'
    xpath_name='//td[@class="name"]/a/text()'#提取品种
    xpath_price = '//td[@class="price"]/text()'  # 提取价格
    xpath_aver = '//td[@class="aver"]/text()'  # 提取均价
    xpath_change = '//td[@class="change"]/text()'  # 提取价格变动
    xpath_today = '//td[@class="today"]/text()'  # 提取价格变动

    page = requests.get(url)
    tree = html.fromstring(page.content.decode('gbk'))
    name= tree.xpath(xpath_name)
    price = tree.xpath(xpath_price)
    aver = tree.xpath(xpath_aver)
    change=tree.xpath(xpath_change)
    today=tree.xpath(xpath_today)
    change.insert(1,-95)
    aver.insert(5,100)

    print()
    data={"name":name,'price':price,'aver':aver,'change':change,'time':today}
    df=pd.DataFrame(data).iloc[:,[2,3,0,1,4]]
    print(df)
    df.to_excel('smm.xlsx')

if __name__=='__main__':
  smm()
