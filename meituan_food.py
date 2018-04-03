from selenium import webdriver
import time
from scrapy.selector import Selector
import urllib.request
import requests
import json
import collections
import re
import traceback
from collections import Counter
'''
def Get_Data(driver,url):
    time.sleep(1)
    driver.get(url)
    data=Selector(text=driver.page_source)
    urlname=urllib.request.unquote(url.split('/')[-1])
    for sel in data.xpath('//div[@class="common-list-main"]/div'):
        fllowurl=sel.xpath('div/div/a/@href').extract_first()
        shopname = sel.xpath('div/div/div/div/a/text()').extract_first()
        address = sel.xpath('//span[@class="address ellipsis"]/text()').extract_first()
        shopdata='%s[}%s[}%s[}%s' %(urlname,fllowurl,shopname,address)
        with open('C:/Users/Administrator/Desktop/meituanshoplist.txt', 'a', encoding='utf-8') as f:
            f.write(shopdata)
            f.write('\n')

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe',chrome_options = options)
driver.set_page_load_timeout(100)
driver.set_script_timeout(100)
driver.get('http://cd.meituan.com/')
time.sleep(5)
success=[]
#Get_Data(driver,'http://cd.meituan.com/s/%E8%9C%80%E9%A3%8E%E9%9B%85%E9%9F%B5')
with open('C:/Users/Administrator/Desktop/meituanshoplist.txt', 'r', encoding='utf-8') as f:
    for line in f:
        success.append('http://cd.meituan.com/s/' + str(line.split('[}')[0]).replace('\n','') )

with open('C:/Users/Administrator/Desktop/20171019_0.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url = 'http://cd.meituan.com/s/' + str(line.split('[}')[0])
        try:
           if url not in success:
               time.sleep(1)
               Get_Data(driver,url)
        except:
             print(url)
             pass
driver.quit()
'''
def GetImg(url,img_name):
    dir='D:/photo/美团资质/'
    urllib.request.urlretrieve(url, '%s%s' % (dir, img_name))

def Get_Html(driver,url):
    '''
    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    headers = {'User-Agent': UserAgent,
               #'Connection': 'keep - alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': 'rvct=59; _lx_utm=utm_campaign%3Dbaidu%26utm_medium%3Dorganic%26utm_source%3Dbaidu%26utm_content%3Dhomepage%26utm_term%3D; _lxsdk_cuid=15f395c1cfec8-02579183068961-c303767-1fa400-15f395c1cffc8; mtcdn=K; lsu=; ci=59; __mta=43291034.1508495859288.1508500612985.1508586109344.7; ppos=30.573148%2C104.009535; pposn=%E9%93%81%E5%85%AC%E9%B8%A1%E8%80%97%E5%84%BF%E9%B1%BC%EF%BC%88%E8%88%AA%E7%A9%BA%E6%B8%AF%E5%BA%97%EF%BC%89; __mta=43291034.1508495859288.1508500612985.1508586111934.7; __utma=211559370.750713271.1508496042.1508498718.1508586112.3; __utmb=211559370.1.10.1508586112; __utmc=211559370; __utmz=211559370.1508496042.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uuid=4c444bc8f12c492f94d0.1508495931.2.0.1; oc=R2H4VmLnBVIcdshYLVkEFL7MLG5mDU6jQF7wC7fCnICVTWEriXmKOI-dlyJEhMKNzV82jv8l_6fz5t_gqT_ZV_5078SpqEP-Y5CwyS8QGszbECWoB4QugnfFdhA22ae78Ha6HnwOMx69UkStMnHUHxbdu8Blk3b9LZebmW0_YBQ; _lxsdk_s=15f3ebd2889-ff3-e23-8a3%7C%7C5'
               }
    # login_url='https://passport.meituan.com/account/unitivelogin?uuid=7fc7dd7ace2f44ae6b68.1508573459.1.0.0&service=www&continue=http%3A%2F%2Fwww.meituan.com%2Faccount%2Fsettoken%3Fcontinue%3Dhttp%253A%252F%252Fcd.meituan.com%252F'
    get_request = requests.get(url, headers=headers)
    get_request.encoding = 'utf-8'
    #print(get_request.text)
    data = Selector(text=get_request.text)
    '''
    driver.get(url)
    time.sleep(1)
    data = Selector(text=driver.page_source)
    print(driver.current_url)
    if  'meishi'  in driver.current_url:
        return data
    elif 'http://cd.meituan.com/'==driver.current_url:
        print('奇怪的现象++++++',url)
        return 0
    elif 'shop' not in driver.current_url:
        return 0
    else:
        return data


def Get_data(driver,fristurl):
    id=fristurl
    type = 'meishi'
    if type=='cate' or type=='yiliao' or type=='bendigouwu' or type=='wanggou'or type=='jiazhuang' or type=='zhenguo' or type=='qinzi':
      url=fristurl
    else:
      url = 'http://cd.meituan.com/shop/%s' % id
    htmldata = Get_Html(driver,url)
    if htmldata==0:
        return 0
    #print(type)
    #print(htmldata.extract())
    Imgname = ''
    iszz = ''
    if type=='meishi':
        #try:
          #shopname=htmldata.xpath('//h2/span[@class="title"]/text()').extract_first().replace('\n','')
        #except:
        shopname = htmldata.xpath('//div[@class="name"]/text()').extract_first().replace('\n', '')
        try:
          iszz = htmldata.xpath('//div[@class="name"]/span/text()').extract_first().replace('\n', '').replace('"', '')
        except:
          iszz=''
        #try:
        #  address=htmldata.xpath('//span[@class="geo"]/text()').extract_first().replace('\n','')
        #except:
        address = htmldata.xpath('//div[@class="address"]/p[1]/text()[2]').extract_first().replace('\n', '').replace('"', '')

        #try:
        #  phone=htmldata.xpath('//div[@class="fs-section__left"]/p[2]/text()').extract_first().replace('\n','')
        #except:
        try:
            phone = htmldata.xpath('//div[@class="address"]/p[2]/text()[2]').extract_first().replace('\n', '').replace('"', '')
        except:
            phone=''

        #try:
        #   time = htmldata.xpath('//div[@class="field-group"][1]/text()[2]').extract_first().replace('\n','').replace(' ','')
        #except:
        try:
            time = htmldata.xpath('//div[@class="address"]/p[3]/text()[2]').extract_first().replace('\n', '').replace('"', '')
        except:
             time = ''
        try:
            zzimg=htmldata.xpath('//div[@class="shop-identity-wrapper"]/a/@data-foodsafe').extract_first()
            imgjson=json.loads(zzimg)
            businessLicenceImg=imgjson['businessLicenceImg'].replace('\\','')
            Imgname=re.sub(r'\||\*|\"|\（|\）','',shopname+ id[0:5] + '_biz_photo.jpg').replace(' ', '')
            GetImg(businessLicenceImg, Imgname)
        except:
            Imgname=''
    elif type=='jiudian':
        shopname = htmldata.xpath('//div/span[@class="fs26 fc3 pull-left bold"]/text()').extract_first().replace('\n', '')
        address = htmldata.xpath('//div[@class="fs12 mt6 mb10"]/span/text()').extract_first().replace('\n', '')
        try:
          phone = htmldata.xpath('//div[@class="mb10"]/text()').extract_first().replace('\n', '')
        except:
          phone=''
        time = ''
    elif type=='xiuxianyule' or type=='jiehun':
        shopname = htmldata.xpath('//h1[@class="seller-name"]/text()').extract_first().replace('\n', '')
        try:
            address = htmldata.xpath('//span[@data-reactid="52"]/text()').extract_first().replace('\n', '')
        except:
            address = htmldata.xpath('//span[@data-reactid="49"]/text()').extract_first().replace('\n', '')
        try:
            phone = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
        except:
            phone = ''
        try:
            time = htmldata.xpath('//span[@data-reactid="59"]/text()').extract_first().replace('\n', '')
        except:
            time = ''
    elif type=='jiankangliren' or type=='shenghuo':
        shopname = htmldata.xpath('//h1[@class="seller-name"]/text()').extract_first().replace('\n','')
        try:
           address = htmldata.xpath('//span[@data-reactid="49"]/text()').extract_first().replace('\n', '')
        except:
           address = htmldata.xpath('//span[@data-reactid="52"]/text()').extract_first().replace('\n', '')
        try:
          try:
             phone = htmldata.xpath('//span[@data-reactid="53"]/text()').extract_first().replace('\n', '')
          except:
             phone = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
        except:
          phone=''
        try:
          try:
            time = htmldata.xpath('//span[@data-reactid="59"]/text()').extract_first().replace('\n', '')
          except:
            time = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
        except:
          time=''
    elif type == 'cate' or type == 'yiliao' or type == 'bendigouwu' or type == 'wanggou':
        shopname = htmldata.xpath('//h1[@class="seller-name"]/text()').extract_first().replace('\n', '')
        try:
          address = htmldata.xpath('//span[@data-reactid="49"]/text()').extract_first().replace('\n', '')
        except:
          try:
            address = htmldata.xpath('//span[@data-reactid="47"]/text()').extract_first().replace('\n', '')
          except:
            address = htmldata.xpath('//span[@data-reactid="52"]/text()').extract_first().replace('\n', '')

        try:
            try:
              phone = htmldata.xpath('//span[@data-reactid="53"]/text()').extract_first().replace('\n', '')
            except:
              phone = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
        except:
            try:
              phone = htmldata.xpath('//span[@data-reactid="51"]/text()').extract_first().replace('\n', '')
            except:
              phone = ''
        try:
            try:
              time = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
            except:
              time = htmldata.xpath('//span[@data-reactid="54"]/text()').extract_first().replace('\n', '')
        except:
            time = ''
    elif type=='jiazhuang':
        try:
          shopname = htmldata.xpath('//h1[@class="shop-title"]/text()').extract_first().replace('\n','')
        except:
          shopname = htmldata.xpath('//h1[@class="shop-title full-name"]/text()').extract_first().replace('\n', '')

        address = htmldata.xpath('//p[@class="shop-contact address"]/span/@title').extract_first().replace('\n', '')
        try:
          phone = htmldata.xpath('//div[@class="shop-contact telAndQQ"]/span/strong/text()').extract_first().replace('\n', '')
        except:
          phone=''
        try:
          time = htmldata.xpath('//p[@class="shop-contact"]/text()').extract_first().replace('\n', '')
        except:
          time=''
    elif type=='zhenguo' or type=='qinzi':
        shopname = htmldata.xpath('//h1[@class="seller-name"]/text()').extract_first().replace('\n', '')
        try:
          address = htmldata.xpath('//span[@data-reactid="48"]/text()').extract_first().replace('\n', '')
        except:
          address = htmldata.xpath('//span[@data-reactid="52"]/text()').extract_first().replace('\n', '')

        try:
            try:
              phone = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
            except:
              phone = htmldata.xpath('//span[@data-reactid="52"]/text()').extract_first().replace('\n', '')
        except:
            phone = ''
        try:
            try:
              time = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
            except:
              time = htmldata.xpath('//span[@data-reactid="56"]/text()').extract_first().replace('\n', '')
        except:
            time = ''


    data = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' % (id,fristurl, shopname, address, phone, time,Imgname, type,iszz)
    with open('C:/Users/Administrator/Desktop/meituandata1115.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')
'''
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
driver = webdriver.Chrome(
    executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe',
    chrome_options=options)
driver.set_page_load_timeout(100)
driver.set_script_timeout(100)
driver.get('http://cd.meituan.com/')
Get_data(driver,' ','http://www.meituan.com/meishi/94140474/')
'''
#'''
#'''
#print(collections.Counter(list))
dailist = []
waitlist = []
with open('C:/Users/Administrator/Desktop/meituanbasic20171113.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # if line.split('[}')[1] != 'None':
        # textname=line.split('[}')[0].replace('\n','')
        turl = line.split('[}')[0].replace('\n', '').replace('-', '')
        waitlist.append(turl)
dailist = set(waitlist)


while True:
    counterlist=[]
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe',
        chrome_options=options)
    driver.set_page_load_timeout(50)
    driver.set_script_timeout(50)
    try:
        success = []
        with open('C:/Users/Administrator/Desktop/meituandata1115.txt', 'r', encoding='utf-8') as f:
            for line in f:
                success.append(line.split('[}')[0])
        print(len(success))
        print(len(set(success)))
        if  len(dailist) <= len(success):
             break
        driver.get('http://cd.meituan.com/')
        time.sleep(3)
        for i in dailist:
            if i not in success:
                Get_data(driver, i)
    except:
        time.sleep(2)
        traceback.print_exc()
        driver.quit()
        continue


