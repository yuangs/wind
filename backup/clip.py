# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 14:11:01 2016

@author: gsyuan
利用requests库下载各种文件
@author: gsyuan
"""

import pandas as pd
import re

def getClipboard():
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    data = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return data


# c=pd.read_excel(r'http://www.dce.com.cn/portal/servlet/look/%B4%F3%C1%AC%C9%CC%C6%B7%BD%BB%D2%D7%CB%F9%CC%FA%BF%F3%CA%AF%D6%B8%B6%A8%BD%BB%B8%EE%B2%D6%BF%E2%C3%FB%C2%BC.xls?filename=tPPBrMnMxre9u9LXy%24nM_r%24zyq%24WuLaovbu47rLWv_LD_8K8LjE0Njg0MDU4NzMxOTAueGxz&cid=1210666139100')

def find_str():
    in_str = getClipboard()
    pattern = input('Please input the pattern string:')
    pattern = pattern
    out_str=re.findall(pattern,in_str)
    return out_str

if __name__=='__main__':
    print(find_str())