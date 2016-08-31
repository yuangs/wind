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
