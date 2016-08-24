# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 14:11:01 2016

@author: gsyuan
利用requests库下载各种文件
@author: gsyuan
"""
import os
import re
import requests
from lxml import etree

#要下载的网页链接
url = 'http://bbs.tianya.cn/post-develop-2168806-1.shtml'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
html = requests.get(url,headers=headers).text
page = etree.HTML(html)
title=page.xpath('/html/head/title/text()')[0]
print(title)

def download(url):
  '下载文件，文件名为url得出'
  #从URL中解析出文件名
  curr_dir = os.getcwd()
  file=title

  print('FILE:',file)
  print('USE: requests')
  print('FROM:',url)
  print('SAVED:',curr_dir)

  #下载数据
  r = requests.get(url,headers=headers)
  print('SIZE:',len(r.content))
  with open(file, "wb") as f:
       f.write(r.content)

if __name__=='__main__':
    download(url)

