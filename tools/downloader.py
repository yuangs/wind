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

if __name__=='__main__':
    download(url)

