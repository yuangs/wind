#-*- encoding: ISO-8859-1 -*-
from lxml import html
import requests
import time

def getblog(u='1619925757',p=5):
    #给定一个用户id和页面的总页数，下载对应页面的博客文章标题和链接的地址
    #可能出现unicode解析错误，我们也一并打印出来
    userId=u
    pageNums=p
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    for i in range(pageNums):
        url='http://blog.sina.com.cn/s/articlelist_%s_0_%d.html' %(userId,i+1)
        page = requests.get(url,headers=headers)
        page.encoding=page.encoding
        tree = html.fromstring(page.text)
        #get the title of the article（使用xpath表达式取得文章和标题的链接地址）
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

        time.sleep(3)

getblog()




