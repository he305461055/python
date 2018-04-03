import DZDP_SPIDERS.dzdp_basic_spider as spider
import os
from selenium import webdriver

def CREATE_FILE(filename):
    file='E:/python/DZDP_SPIDERS/%s_variable.txt' %filename
    if os.path.exists(r'%s' % file):
        pass
    else:
        with open(file, 'w', encoding='utf-8') as f:
            pass

#CREATE_FILE('basic_list')
#CREATE_FILE('detail_address')
spider.GET_BASIC('dzdp','basic_list','http://www.dianping.com/search/category/8/10/g0r0')
#spider.GET_BASIC('dzdp','basic_list','http://www.dianping.com/search/category/8/10/g210r1596')

