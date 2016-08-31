# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 14:11:01 2016

@author: gsyuan
利用requests库下载各种文件
@author: gsyuan
"""
def getClipboard():
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    data = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return data


def setClipboard(aString):
    import win32clipboard as w
    import win32con
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()
    return aString

if __name__=='__main__':
  print(getClipboard())
