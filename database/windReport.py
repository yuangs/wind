# -*- coding: utf-8 -*-
'先将报告网址通过fiddler下载到桌面文件中，然后遍历文件，下载万得研究报告'
import re
import requests
from urllib import parse


files=open(r"C:\Users\Administrator\Desktop\report.txt",encoding='utf-8').readlines()


def download_report(url,title,doctype):
    path=r'D:\aliyun\Work\zjt\%s' %title
    print('to: '+path)
    response = requests.get(url)
    with open(path+'.'+doctype, 'wb') as f:
        f.write(response.content)

for raw_url in files:
    url=raw_url.strip('\n')
    url=parse.unquote(str(url))
    print('From: ' +url)
    if url.find('__biz')==-1:
        title=re.search('(?<=bulletin/).*?(?=\.)',str(url)).group()
        doctype=re.search('(?<=\.)\w{3,4}?(?=\?)',str(url)).group()
        print('Downloading this file:  '+title)
        try:
            download_report(url,title,doctype)
            print('Sucessful!')
        except:
         print("error:%s\n" %(url))