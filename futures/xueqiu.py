import os,re
import requests
from lxml import etree
url='https://xueqiu.com/today/all'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/51.0.2704.106 Safari/537.36'}

r=requests.get(url,headers=headers)
selector = etree.HTML(r.content)
titles=selector.xpath("//div[@class='list_item_tit']/a/text()")
links=selector.xpath("//div[@class='list_item_tit']/a/@href")

# for i in range(len(titles)):
#     print(titles[i]+'--> https://xueqiu.com'+links[i])

def qilin():
    for i in range(15):
        url='http://www.qilinfengxian.com/Columnist/Default2.php?PageNo=%s' %i
        selector=etree.HTML(requests.get(url,headers=headers).content)
        titles = selector.xpath("//*[@id='"'DIVOrder2'"']/div[1]/ul/li[2]/a/text()")
        links = selector.xpath("//*[@id='"'DIVOrder2'"']/div[1]/ul/li[2]/a/@href")
        for j in range(len(titles)):
            print(titles[j] + '-->' + links[j])


qilin()