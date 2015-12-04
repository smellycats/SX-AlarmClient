#-*- coding:UTF-8 -*-
import sys
import time
import webbrowser
sys.path.append("libs")

 

url = 'http://www.baidu.com'
url2 = 'http://www.jd.com'
webbrowser.register('firefox', None)
webbrowser.open_new_tab(url)
print webbrowser.get()
time.sleep(5)
webbrowser.open_new_tab(url2)
#help(webbrowser)
