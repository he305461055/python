from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector

def get1(driver ,regsion):
    time.sleep(1)
    url='http://cd.meituan.com/meishi/'+regsion.split('/')[1]+'/'
    driver.get(url)
    button='//span/b[text()="'+regsion.split('/')[0]+'"]'
    driver.find_element_by_xpath(button).click()
    data=Selector(text=driver.page_source)
    for sel in data.xpath('//ul[@class="clear"]/li'):
         smallregoin=sel.xpath('a/@href').extract_first()
         name=sel.xpath('a/text()').extract_first()
         if name=='全部':
             continue
         d='%s[}%s[}%s[}%s' %(regsion.split('/')[0],regsion.split('/')[1],str(smallregoin).split('/')[-2],name)
         with open('C:/Users/Administrator/Desktop/regsion.txt', 'a', encoding='utf-8') as f:
             f.write(d)
             f.write('\n')


chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)
driver.get('http://cd.meituan.com/')

regsion=['郫县/b3805','温江区/b3798','龙泉驿区/b3795','青白江区/b3796','彭州市/b3800','新津县/b3808','都江堰市/b3799','新都区/b3797',
          '邛崃市/b3801','崇州市/b3802','金堂县/b3803','大邑县/b3806','双流区/b5896','蒲江县/b3807']
for i in regsion:
    get1(driver,i)

