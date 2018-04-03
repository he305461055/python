from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector

datatime=str(time.strftime("%Y%m%d", time.localtime(time.time())))

def get(driver,ci):
    data=Selector(text=driver.page_source)
    for sel in data.xpath('//div[@class="result"]/div[@class="box-result clearfix"]'):
         url=sel.xpath('div/h2/a/@href').extract_first()
         if url is None:
             continue
         data='%s[}%s' %(url,ci)
         with open('C:/Users/Administrator/Desktop/%s.txt' %datatime, 'a', encoding='utf-8') as f:
            f.write(data)
            f.write('\n')


ciku=['3D城市','3D店铺','3D商城','3D沙盘','3D社交','3D互联网','3D景区','3D景区旅游O2O','3D政务','3D地图','大数据','虚拟现实','实景店铺','全景地图','三维动态视景','实体行为','真实感模拟',
'AR景区','AR旅游','AR技术','AR原理','AR现实增强','VR经济','vr虚拟现实','VR体验','vr资源','vr技术','VR原理']

#driver.get('http://www.sina.com.cn/')
#time.sleep(2)
def get_url():
    for ci in ciku:
        time.sleep(1)
        url='http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%s&from=home&ie=utf-8' %ci
        driver.get(url)
        get(driver,ci)
       # for i in range(2):
       #     try:
       #         get(driver,ci)
       #         time.sleep(1)
       #         driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
       #         driver.find_element_by_xpath('//a[@title="下一页"]').click()
       #     except:
       #         print(ci)
       #         continue

def get_content(driver,url,ci):
    if not os.path.exists('C:/Users/Administrator/Desktop/%s/'%datatime):
        os.makedirs('C:/Users/Administrator/Desktop/%s/'%datatime)
    if not os.path.exists('C:/Users/Administrator/Desktop/%s/%s/'%(datatime,ci)):
        os.makedirs('C:/Users/Administrator/Desktop/%s/%s/'%(datatime,ci))
    driver.get(url)
    time.sleep(1)
    data  = Selector(text=driver.page_source)
    title = data.xpath('//h1/text()').extract_first()
    shtml = data.xpath('//div[@id="artibody"]|//div[@id="article"]').extract_first()
    if shtml is None:
        print(url+'是空')
    else:
        sdata='<!DOCTYPE html><html><body><h1>%s</h1>%s</body></html>' %(title,shtml)
        with open('C:/Users/Administrator/Desktop/%s/%s/%s.html' %(datatime,ci,title), 'a', encoding='utf-8') as f:
            f.write(sdata)
            f.write('\n')
        with open('C:/Users/Administrator/Desktop/%s/标题对应URL.txt' %(datatime), 'a', encoding='utf-8') as f:
            f.write('%s[}%s' %(title,url))
            f.write('\n')
    success.append(url)
    with open('C:/Users/Administrator/Desktop/success.txt.', 'a', encoding='utf-8') as f:
        f.write(url)
        f.write('\n')

chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)

get_url()

success=[]
with open('C:/Users/Administrator/Desktop/success.txt', 'r', encoding='utf-8') as f:
    for line in f:
        success.append(line.replace('\n',''))

with open('C:/Users/Administrator/Desktop/%s.txt' %datatime, 'r', encoding='utf-8') as f:
    for line in f:
        url=line.split('[}')[0].replace('\n','')
        ci=line.split('[}')[1].replace('\n','')
        if url not in success:
            try:
              get_content(driver,url,ci)
              success = []
              with open('C:/Users/Administrator/Desktop/success.txt', 'r', encoding='utf-8') as f:
                  for line in f:
                      success.append(line.replace('\n', ''))
            except:
              print(url,ci)
              driver.quit()
              chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
              os.environ["webdriver.chrome.driver"] = chrome_driver
              driver = webdriver.Chrome(chrome_driver)
              continue
