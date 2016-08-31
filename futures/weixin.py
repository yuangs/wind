
import downloader
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

pattern='<h4 class="msg_title" hrefs="(.*?)">'
content=getClipboard()
urls=re.findall(pattern,content)
for url in urls:
    print(urls)

