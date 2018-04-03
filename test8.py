from selenium import webdriver
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import os

url_list=[]
def get_url(drivcer):
    data = driver.page_source
    sdata=Selector(text=data)
    url=sdata.xpath('//*[@id="listContent"]/a/@href').extract()
    for i in url:
        url_list.append(i)
    driver.find_element_by_xpath('//*[@id="list_pagination"]/a[last()]').click()
    time.sleep(3)
    driver.quit

def get_data(driver,fllow_url):
    url='http://www.mafengwo.cn'+fllow_url
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    #driver.execute_script("window.scrollBy(100000,document.body.scrollHeight)","1000")#向下滚动到页面底部
    js = "var q=document.body.scrollTop=1000"
    driver.execute_script(js)

    #name=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/h1').text
    shopname=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[1]/div[2]/div/a').text
    try:
      phone=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[1]/div[2]/ul/li[2]/span[1]').text
    except:
      phone=''
    data='%s}%s' %(shopname,phone)
    with open('C:/Users/Administrator/Desktop/旅游/feizhu.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')


chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)
driver.set_page_load_timeout(100)
driver.set_script_timeout(100)
#url = 'http://www.mafengwo.cn/sales/0-10035-0-1-0-0-0-0.html?group=1&kw=&seid=14B0690E-E9A3-45B3-8E5E-AECBA8AF145C&group=1'
url='https://market.fliggy.com/markets/h5/alitripzhuanxian'
driver.get(url)
time.sleep(70)
data = driver.page_source
sdata = Selector(text=data)
for sel in  sdata.xpath('//a[@class="goods-detail pdlr10"]'):
     url=sel.xpath('@href').extract_first()
     name=sel.xpath('div[1]/text()').extract_first()
     price=''.join(sel.xpath('div[3]/span/*/text()').extract())
     data='%s[}%s[}%s' %(url,name,price)
     with open('C:/Users/Administrator/Desktop/旅游/feizhu.txt', 'a', encoding='utf-8') as f:
         f.write(data)
         f.write('\n')
driver.quit()
#for i in range(12):
#    get_url(driver)

#for fllow_url in url_list:
#    get_data(driver,fllow_url)