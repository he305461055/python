from selenium import webdriver
from bs4 import BeautifulSoup
import html.parser
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

html_parser = html.parser.HTMLParser()
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.resourceTimeout"] = 1000
driver=webdriver.PhantomJS(executable_path='D:/Python35/phantomjs',desired_capabilities=cap)
driver.get('http://www.dianping.com/shop/32877996')
time.sleep(5)
data=driver.page_source
data = html_parser.unescape(data)
soup=BeautifulSoup(data,'html.parser')
shop_name=soup.find('h1',class_='shop-name').next.replace('\n','')
print(shop_name)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'body')))
print(data)

button=driver.find_element_by_xpath('//*[@id="basic-info"]/a')
if button:
    button.click()
    print('true')
    #shop_time=driver.find_element_by_xpath('//*[@id="rev_317558223"]/div/div[2]').text
    content=soup.find('ul',class_='comment-list J-list').find_all('li')[0].find('div',class_='content').find('div',class_='info J-info-all').find('p').next.replace('\n','')
    print(content)
    driver.quit()
else:
    print('flase')