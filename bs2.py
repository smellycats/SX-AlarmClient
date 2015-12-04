#!/usr/bin/env python
#encoding:utf8
#author: linuxhub.org
 
from selenium import webdriver
import time
 
url = 'http://www.baidu.com'
url2 = 'http://localhost'
BrowserObj_dirver = webdriver.Firefox()
BrowserObj_dirver.get(url)
print 'done'
time.sleep(5)
BrowserObj_dirver.get(url2)

#BrowserObj_dirver.quit()
#BrowserObj_dirver.close()
