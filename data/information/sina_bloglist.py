#-*- encoding: UTF-8 -*-
from lxml import html
import requests
import time

def sinabloglist(u='1619925757',p=2):
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

        time.sleep(4)


if __name__=='__main__':
  sinabloglist()
