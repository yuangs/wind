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

def getblog(blog_id='1619925757'):
    
    url_all=[]
    for i in range(54):
        page='http://blog.sina.com.cn/s/articlelist_%s_0_%s.html' %(blog_id,i)
        r=requests.get(page)
        url_page=re.findall('http://blog.sina.com.cn/s/blog_.*.html',r.content.decode('utf-8'))
        url_all.extend(url_page)
    print(url_all)
    for i in url_all:
        download(i)
        


url = 'http://www.dce.com.cn/portal/uploadFiles/296.1469674883750.jpg'
curr_dir=os.getcwd()


def download(url):
  '''
  下载文件
  '''
  #从URL中解析出文件名
  file=url.split(sep='/')[-2]+'_'+url.split(sep='/')[-1]
  if not '.' in file:file=file+'.html'

  headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
  print('FILE:',file)
  print('USE: requests')
  print('FROM:',url)
  print('SAVED:',curr_dir)

  #下载数据
  r = requests.get(url,headers=headers)
  print('SIZE:',len(r.content))
  with open(file, "wb") as f:
       f.write(r.content)


def cffexoi(date='0811'):
  date=date
  url='http://www.cffex.com.cn/fzjy/ccpm/2016%s/%s/IF_1.csv' %(date[0:2],date[-2:])
  download(url)

def shfeoi():
  dates=['20160104','20160105']
  for date in dates:
    url='http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat' %date
    download(url)


if __name__=='__main__':
    
    getblog()
    
#    for i in url_all:
#        download(i)

#  shfeoi()
