
import time
import requests
import re

def getClipboard():
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    data = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return data

def article_urls():
    #将微信公众号电脑页面复制到剪贴板，并获取urls,保存至文件
    content=getClipboard()
    pattern='<h4 class="msg_title" hrefs="(.*?)">'
    if re.search(pattern,content):
        urls=re.findall(pattern,content)
    else:
        pattern='<h4 class="msg_desc" hrefs="(.*?)">'
        urls = re.findall(pattern, content)

    with open(r"C:\Users\gsyuan\Desktop\url.txt",'w') as f:
        for url in urls:
            url=re.sub('&amp;','&',url)
            f.write(url+'\n')

if __name__ == '__main__':
    article_urls()

