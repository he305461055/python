from selenium import webdriver
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time

url_list=[]
def get_data(driver):
     #data=Selector(text=aa)
     data = driver.page_source
     soup = BeautifulSoup(data, "html.parser")#//*[@id="_prd"]/div[2]/div[2]/h2/a
     for res in soup.find('div',attrs={'id':'_prd'}).find_all('div',attrs={'class':'main_mod product_box flag_product '}):
          url=res.find('div',attrs={'class':'product_main'}).find('h2').find('a')['href']#.get('href')
          url_list.append(url)

driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe')
#driver.set_page_load_timeout(100)
#driver.set_script_timeout(100)
#url = 'http://vacations.ctrip.com/grouptravel-28B64DC28P1/?searchValue=%E5%91%A8%E8%BE%B9&searchText=%E5%91%A8%E8%BE%B9#_flta'
start_urls=[]
fllow_urllist=[]
with open('C:/Users/Administrator/Desktop/旅游/phonelist.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url = line.split('}')[0]
        fllow_urllist.append(url)
with open('C:/Users/Administrator/Desktop/旅游/list.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url = 'http://%s' % line.replace('\n', '')
        if url not in fllow_urllist:
            start_urls.append(url)
print(len(start_urls))
for url in start_urls:
    driver.get(url)
    time.sleep(3)
    try:
      fllow_url = driver.find_element_by_xpath('//a[@class="provider_name"]').get_attribute('href')
    except:
      try:
        fllow_url = driver.find_element_by_xpath('//*[@id="providerID"]/span/a').get_attribute('href')
      except:
        continue
    driver.get(fllow_url)
    time.sleep(3)
    name1=driver.find_element_by_xpath('//*[@id="supplierContainer"]/div[1]/div/div[1]/p').text
    try:
      name2=driver.find_element_by_xpath('//*[@id="supplierContainer"]/div[1]/div/div[2]/ul/li[1]').text
    except:
      name2=''
    try:
      name3=driver.find_element_by_xpath('//*[@id="supplierContainer"]/div[1]/div/div[2]/ul/li[2]').text
    except:
      name3=''
    try:
      phone=driver.find_element_by_xpath('//*[@id="supplierContainer"]/div[1]/div/span/span').text
    except:
      continue
    data='%s}%s}%s}%s}%s}%s' %(url,fllow_url,name1,name2,name3,phone)
    with open('C:/Users/Administrator/Desktop/旅游/phonelist.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

'''
for i in range(100):
    get_data(driver)
    driver.find_element_by_xpath('//*[@id="_pg"]/a[11]').click()
    time.sleep(5)

driver.quit()
url_list=set(url_list)
for url in url_list:
    with open('C:/Users/Administrator/Desktop/旅游/list.txt','a',encoding='utf-8') as f:
        f.write(url)
        f.write('\n')
'''
