from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
#import mysql入库 as mysqltool

def get_data(driver,name):
    data = Selector(text=driver.page_source)

    for res in data.xpath('//*[@id="poilist"]/div'):
        url=res.xpath('a/@href').extract_first()
        shopname=res.xpath('div[@class="content"]/*/div[1]/div/text()').extract_first()
        if 'None'==shopname:
            continue
        star=','.join(res.xpath('div[@class="content"]/*/div[2]/div[1]/i/@class').extract())
        shopsold=res.xpath('div[@class="content"]/*/div[2]/div[2]/text()').extract_first()
        shopright=res.xpath('div[@class="content"]/*/div[2]/i[1]/text()').extract_first()
        shoptime=res.xpath('div[@class="content"]/*/div[2]/i[3]/text()').extract_first()
        sendprice=''.join(res.xpath('div[@class="content"]/*/div[3]/span[1]/em/text()').extract())
        deliveryfee=''.join(res.xpath('div[@class="content"]/*/div[3]/span[2]/text()').extract())

        shopdata='%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' %(url,shopname,star,shopsold,shopright,shoptime,sendprice,deliveryfee,name)
        with open('C:/Users/Administrator/Desktop/美团外卖/shoplist_%s_1.txt' %name, 'a', encoding='utf-8') as f:
            f.write(shopdata)
            f.write('\n')

'''
    for i in range(0,9):
        driver.find_element_by_xpath('//*[@id="loading"]/div').click()
        time.sleep(5)

    data=driver.page_source
    soup=BeautifulSoup(data,"html.parser")
    list_data=soup.find('ul',attrs={'class':'list clearfix'}).find_all('li',attrs={'class':'fl rest-li'})
    for res in list_data:
        shop_id=res.find('a',attrs={'class':'rest-atag'}).get('href')
        with open('C:/Users/Administrator/Desktop/list.txt', 'a', encoding='utf-8') as f:
            f.write(shop_id)
            f.write('\n')




#url='http://i.waimai.meituan.com/home?lat=30.541111&lng=104.059155'
urllist=[#'http://i.waimai.meituan.com/home?lat=30.627222&lng=104.06055,玉林',
         #'http://i.waimai.meituan.com/home?lat=30.634774&lng=104.031921,紫荆',
         #'http://i.waimai.meituan.com/home?lat=30.619286&lng=104.075643,科华',
         #'http://i.waimai.meituan.com/home?lat=30.622109&lng=104.098407,锦华',
         #'http://i.waimai.meituan.com/home?lat=30.632749&lng=104.029313,红牌楼',
         #'http://i.waimai.meituan.com/home?lat=30.645977&lng=104.033134,双楠',
         #'http://i.waimai.meituan.com/home?lat=30.670267&lng=103.978478,光华',
         #'http://i.waimai.meituan.com/home?lat=30.681726&lng=104.012659,金沙',
         #'http://i.waimai.meituan.com/home?lat=30.705653&lng=104.013817,茶店子',
         #'http://i.waimai.meituan.com/home?lat=30.690691&lng=104.047379,老会展',
         #'http://i.waimai.meituan.com/home?lat=30.697218&lng=104.073694,北站',
         #'http://i.waimai.meituan.com/home?lat=30.677707&lng=104.096474,府青',
         #'http://i.waimai.meituan.com/home?lat=30.669313&lng=104.11071,建设路',
         #'http://i.waimai.meituan.com/home?lat=30.644231&lng=104.119188,万年场',
         'http://i.waimai.meituan.com/home?lat=30.646149&lng=104.109381,双桥',
        ]

url='http://waimai.meituan.com/home/wm6n2ev4q1x5'
chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)
driver.get(url)
get_data(driver)
driver.quit()

file_name='shoplist_%s' %urllist[0].split(',')[1]
for url in urllist:
        mobileEmulation = {'deviceName': 'iPhone 6 Plus'}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe', chrome_options=options)
        driver.set_page_load_timeout(100)
        driver.set_script_timeout(100)
        driver.get(url.split(',')[0])
        time.sleep(5)
        #driver.maximize_window()
        driver.find_element_by_xpath('//*[@id="primary_item_bar_new"]/a[1]/img').click()
        time.sleep(5)
        for i in range(80):
            #driver.execute_script("window.scrollBy(0,200)", "")  # 向下滚动200px
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#向下滚动到页面底部
            time.sleep(3)
        get_data(driver,url.split(',')[1])
        driver.quit()

#sql='insert into meituanshop(url,shopname,star,shopsold,shopright,shoptime,startprice,deliveryfee,CBD) values'
#mysqltool.get_sql(sql,file_name)
'''
def get_img(driver,line):
    id = line.split('[}')[1].replace('\n', '')
    url = 'http://www.dianping.com/shop/%s' % str(id)
    time.sleep(1)
    driver.get(url)
    data=Selector(text=driver.page_source)
    id = url.split('/')[-3]
    id1 = line.split('[}')[0].replace('\n', '')
    name = line.split('[}')[2].replace('\n', '')
    imglist = []
    try:
        for sel in data.xpath('//div[@class="shop-tab-recommend J-panel"]/ul/li'):
            imglist.append(sel)
        for sel in imglist:
            imgurl = sel.xpath('img/@src').extract_first()
            goods = sel.xpath('img/@alt').extract_first()
            if goods == None:
                continue
            img = '%s_photo_%d.jpg' % (name, imglist.index(sel))
            print(goods, imgurl)
            imgdata = '%s[}%s[}%s[}%s[}%s' % (id1, id, name, goods,img)
            print(imgdata)
            # tool.GetImg(imgdir3, imgurl, img)
            # with open('C:/Users/Administrator/Desktop/shangping_20171106.txt', 'a', encoding='utf-8') as f:
            #    f.write(imgdata)
            #    f.write('\n')
    except:
        print(url)



chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)
driver.get('http://www.dianping.com/citylist')

start_urls=[]
with open('C:/Users/Administrator/Desktop/20171103.txt', 'r', encoding='utf-8') as f:
    for line in f:
        start_urls.append(line.replace('\n', ''))

get_img(driver,'183[}10333429[}MorningHouse')