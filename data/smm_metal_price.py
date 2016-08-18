#-*- encoding: UTF-8 -*-
from lxml import html
import requests
import time
import pandas as pd

def sinablog(u='1619925757',p=5):
    '''
    根据用户id与文章总页数获取新浪博客的标题及链接,e.g.
    http://blog.sina.com.cn/s/articlelist_1619925757_0_1.html
    娱乐工业
    http://blog.sina.com.cn/s/blog_608e1afd0102wkw4.html
    咸吃萝卜扯扯淡
    http://blog.sina.com.cn/s/blog_608e1afd0102wkt2.html
    '''
    userId=u
    pageNums=p
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    for i in range(pageNums):
        url='http://blog.sina.com.cn/s/articlelist_%s_0_%d.html' %(userId,i+1)
        page = requests.get(url,headers=headers)
        page.encoding=page.encoding
        tree = html.fromstring(page.text)
        #get the title of the article
        titles = tree.xpath(r"//*[@id='module_928']/div[2]/div[1]/div[2]/div[*]/p[1]/span[2]/a/text()")
        #get the link of the article
        links=tree.xpath(r"//*[@id='module_928']/div[2]/div[1]/div[2]/div[*]/p[1]/span[2]/a/@href")
        print(url)

        try:
            for j in range(len(titles)):
                print (titles[j].encode('ISO-8859-1').decode("utf-8"))
                print(links[j])
        except Exception as e :
            print(i)
            print(e)

        time.sleep(5)

def smm():
    '''获取smm的每日有色金属报价数据,e.g.
            name           price     aver change   time
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
  sinablog()
  smm()
