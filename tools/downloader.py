# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 14:11:01 2016

@author: gsyuan
利用requests库下载各种文件
@author: gsyuan
"""
import os,re
import requests
from lxml import etree

def save(url):
    """
    给出一个网址，保存网页或文件
    :param url:
    :return: 网页标题或者文件名
    """
    url = url
    curr_dir = os.getcwd()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    def title():
        if re.findall('\.(\w*)?',url)[-1] not in ['doc','docx','xls','xlsx','pdf','rar','ppt','pptx']:
            try:
                html = requests.get(url,headers=headers).text.encode('ISO-8859-1')#服务器返回数据默认编码为：ISO-8859-1
            except:
                html = requests.get(url, headers=headers).text
            page = etree.HTML(html)
            title=page.xpath('/html/head/title/text()')[0]
        else:
            title=os.path.basename(url)
        return title

    title=title()

    def file_name():
        '获得文件名'
        # 以网页形式保存文件
        if isinstance(url[-1], int):
            file = title + '.html'
        elif 'html' in url[-4]:
            file = title + '.html'
        else:
            file = title
        return file

    file=file_name()

    def download():
        print('FILE:',file)
        print('USE: requests')
        print('FROM:',url)
        print('SAVED:',curr_dir)
        # 下载数据
        r = requests.get(url,headers=headers)
        # print('SIZE:',len(r.content))
        with open(file, "wb") as f:
            f.write(r.content)

    download()

if __name__=='__main__':
    # 测试下载链接，要下载的网页链接，获取网页标题
    # 格隆汇 http://www.gelonghui.com/p/84066.html
    # 财新网 http://finance.caixin.com/2016-08-24/100981248.html
    # 华尔街见闻 http://wallstreetcn.com/node/259499
    # 雪球 https://xueqiu.com/today/all
    # 知乎 https://www.zhihu.com/question/27434092
    # 中期协 http://www.cfachina.org/CXFW/zgsyw/ywgzzgs/201512/P020160104519469842030.doc
    # http://www.cfachina.org/CXFW/zgsyw/ywgzzgs/201512/P020160104519470578820.xls
    def download_htmls():
        python=open(r"C:\Users\gsyuan\Desktop\url.txt",'r').readlines()
        python = [item.strip() for item in python]
        for url in python:
            try:
                save(url)
            except:
                pass

    def test():
        urls = ['http://pmi.caixin.com/2016-08-24/100981097.html',
                'http://www.cfachina.org/CXFW/zgsyw/ywgzzgs/201512/P020160104519469842030.doc',
                'http://www.cfachina.org/CXFW/zgsyw/ywgzzgs/201512/P020160104519470578820.xls']

        for url in urls:
            try:
                save(url)
            except:
                pass
    # test()
    download_htmls()







