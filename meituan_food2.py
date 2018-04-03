import re
import csv
import random
import urllib.request
import http.cookiejar
import urllib.parse
import time
import socket
import html.parser
#import regex as re
from collections import deque
from selenium import webdriver
from openpyxl import Workbook
from openpyxl import load_workbook
from  openpyxl.workbook  import  Workbook
from openpyxl.utils import get_column_letter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#影藏IP
def open_socket_web():
    #'124.240.187.84','139.196.108.68','122.114.36.13','182.90.252.10',
         IP=['122.96.59.106:81']
         PROXY = random.choice(IP)#"122.96.59.106:81" # IP:PORT or HOST:PORT
         chrome_options = webdriver.ChromeOptions()
         chrome_options.add_argument('--proxy-server=%s' % PROXY)
         #driver = webdriver.Chrome(chrome_options=chrome_options)
         driver = webdriver.Chrome()
         return driver

#总信息
def collect_info(url):
    driver = open_socket_web()
    driver.set_page_load_timeout(100)
    driver.set_script_timeout(100)
    driver.get(url)
    time.sleep(5)
    ##模拟鼠标往下滑动
    try:
        # driver.execute_script("window.scrollTo(10000, document.body.scrollHeight);")
        driver.find_element_by_css_selector("[gaevent=\"content/page/next\"]").send_keys(Keys.TAB)
        time.sleep(5)
        driver.find_element_by_css_selector("[gaevent=\"content/page/next\"]").send_keys(Keys.TAB)
        time.sleep(5)
        driver.find_element_by_css_selector("[gaevent=\"content/page/next\"]").send_keys(Keys.TAB)
        time.sleep(5)
        # driver.find_element_by_css_selector("[gaevent=\"content/page/next\"]").send_keys(Keys.TAB)
        # time.sleep(5)
        # driver.find_element_by_css_selector("[gaevent=\"content/page/next\"]").send_keys(Keys.TAB)
        # time.sleep(5)
        # driver.execute_script("window.scrollTo(0, 0);")
        # time.sleep(5)
        # driver.execute_script("window.scrollTo(10000, document.body.scrollHeight);")
        # time.sleep(5)
    except:
        pass
    try:
        # data = driver.find_element_by_xpath("//html").get_attribute("outerHTML")
        data = driver.page_source
        html_parser = html.parser.HTMLParser()
        data = html_parser.unescape(data)
        if data.strip() != '':
            print('有数据')
        else:
            return -1
    except:
        print('没有得到数据')
        return -1
    finally:
        driver.quit()
    return data


#爬取美团美食首页
def meituan_frist(url):
        data=collect_info(url)
        #pattern  = re.compile( '(?<=src=")([^"]+\.jpg)[^"]*(?=")')
        #aa = re.compile( '<img class="J-webp" src="(.*?.jpg).*?"')
        #aaa = re.compile('<img class="lazy-img J-webp".*? data-src="(.*?.jpg).*?"')
        pattern  = re.compile(r'(?<=src=")[^"@]+(?:.jpg)')
        pattern1 = re.compile( '<a class="link f3 J-mtad-link" href="(.*?)"')
        pattern2 = re.compile( '<a class="link f3 J-mtad-link" .*?>(.*?)</a>')
        pattern3 = re.compile( '<span class="num">(.*?)</span>')
        pattern4 = re.compile( '<span class="price">¥(.*?)</span>')
        pattern5 = re.compile( '<span class="prefix">.*?</span>(.*?)</span>')

        img_address = re.findall(pattern, data) #图片地址

        shop_address = re.findall(pattern1, data)  # 店铺地址

        shop_name = re.findall(pattern2, data)  # 店铺名称

        rated_num = re.findall(pattern3, data)  # 评价人数

        avg_price = re.findall(pattern4, data)  # 人均价位

        mix_price = re.findall(pattern5, data)  # 最低价位

        for i in range(0,len(img_address)):
            img_address[i]='D:/photo/%s' % img_address[i].split('/')[-1]
        for i in range(0,len(rated_num)):
            rated_num[i]='%s人评价' % rated_num[i]
        for i in range(0, len(avg_price)):
            avg_price[i]='人均%s元' % str(avg_price[i])
        for i in range(0, len(mix_price)):
            mix_price[i]='%s元起' % (mix_price[i])

        items=zip(shop_address,shop_name,rated_num,avg_price,mix_price)
        food_first_list = list(items)
        news_ids = list(set(food_first_list))
        news_ids.sort(key=food_first_list.index)
        food_first_list = news_ids
        print(food_first_list)
        return food_first_list

#进入店铺里爬出店铺信息
def shop_info(url):
    driver = open_socket_web()
    driver.set_page_load_timeout(100)
    driver.set_script_timeout(100)
    driver.get(url)
    time.sleep(5)
    try:
     element = driver.find_element_by_css_selector("a[class=\"J-toggle-biz-info\"]").click()
     pattern9 = re.compile('<span class="long-biz-info">(.*?)<a.*?>.*?</a>', re.S)  # 商铺介绍
    except:
     pattern9 = re.compile('<span class="long-biz-info">(.*?)</span>', re.S)  # 商铺介绍

    time.sleep(5)
    try:
        # data = driver.find_element_by_xpath("//html").get_attribute("outerHTML")
        data = driver.page_source
        #html_parser = html.parser.HTMLParser()
        #data = html_parser.unescape(data)
        if data.strip() != '':
            print('有数据')
        else:
            return -1
    except:
        print('没有得到数据')
        return -1
    finally:
        driver.quit()

    #pattern = re.compile('<span class="title">(.*?)</span>')#店铺名称
    #shop_name=re.findall(pattern,data)
    #shop_name.remove(shop_name[1])
    shop_id=[]
    shop_id.append(url.split('/')[-1])

    pattern1 = re.compile('<span class="geo">(.*?)</span>')#店铺地址
    shop_address = re.findall(pattern1, data)
    for i in range(len(shop_address) - 1):
        shop_address.remove(shop_address[1])

    pattern2 = re.compile('<p class="under-title">(.*?)</p>')#店铺电话
    shop_phone = re.findall(pattern2, data)

    shop_sorce=[]
    pattern3 = re.compile('<strong>(.*?)</strong>')#店铺分数
    shop_sorce = re.findall(pattern3, data)
    for i in range(len(shop_sorce) - 1):
        shop_sorce.remove(shop_sorce[1])

    #pattern4 = re.compile('<a href=".*?" target=_blank class=tag[.*？]?>(.*?)</a>')#店铺类型
    #shop_type = re.findall(pattern4, data)
    pattern5 = re.compile('<div>消费人数 <span class="num">(.*?)</span>')#总消费人数
    consume_people = re.findall(pattern5, data)

    try:
        pattern6 = re.compile('<span class="field-title">营业时间：</span>(.*?)</div>', re.S)  # 营业时间
        shop_time = re.findall(pattern6, data)
        shop_time[0] = shop_time[0].replace('\n', '').strip()
    except:
        shop_time = [' ']

    try:
        shop_service=[]
        pattern7 = re.compile('<span class="inline-item">\s*([\s\S]*?)\s*</span>',re.S)  # 门店服务
        items7 = re.findall(pattern7, data)
        items7[0]=';'.join(items7)
        shop_service.append(items7[0])
    except:
        shop_service = [' ']

    try:
        shop_introduce = re.findall(pattern9, data)# 商铺介绍
        shop_introduce[0]=shop_introduce[0].replace('\n','').strip()
    except:
        shop_introduce=[' ']

    patten1 = re.compile('<img src="([^"@]+\.(?:jpg|png|gif))')#店铺图片
    shop_photo = re.findall(patten1, data)
    img_address=[]
    img_address.append(shop_photo[0].split('/')[-1])

    img_name=shop_photo[0].split('/')[-1]

    # 下载图片
    conn = urllib.request.urlopen(shop_photo[0])
    img = conn.read()
    with open('D:/photo/%s' % img_name, 'wb') as f:
        f.write(img)
    '''
        for i in shop_photo:
            filename = i.split('/')[-1]
            #print('aa=' + i)
            conn = urllib.request.urlopen(i)
            img = conn.read()
            with open('D:/photo/%s' % filename, 'wb') as f:
                f.write(img)
    '''

    items = zip(shop_id, shop_address, shop_phone, shop_sorce, consume_people,shop_time,shop_service,shop_introduce,img_address)
    shop_list=list(items)

#写入文件
    try:
        with open('C:/Users/Administrator/Desktop/shop.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in shop_list:
             spamwriter.writerow(i)
        time.sleep(10)
    except:
        with open('C:/Users/Administrator/Desktop/shop.txt', 'a', encoding='utf-8') as f:
            # spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for v1, v2, v3, v4, v5, v6, v7, v8, v9 in shop_list:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (v1, v2, v3, v4, v5, v6, v7, v8, v9))
                f.write('\n')



#拿到用户评论等信息
#def user_content(url):
    try:
        pattern = re.compile('<span class="name vip_level_high">(.*?)</span>')#评论用户用户名
        user_name = re.findall(pattern, data)
    except:
        user_name = [' ']
    try:
        pattern1 = re.compile('<p\sclass="content".*?>\s*(?:<a.*?</a>)?\n(.*?)</p>',re.S)#用户评论
        #pattern1 = re.compile('<p class="content">(?:.*?<a.*?><strong.*?</s.*?</a>)?(.*?)</p>',re.S)
        user_content = re.findall(pattern1, data)
        for i in range(0, len(user_content)):
            user_content[i] = user_content[i].replace('\n','').strip()
    except:
        user_content = [' ']

    try:
        pattern8 = re.compile('<div class="rate-status">.*?<span class="common-rating"><span class="rate-stars" style="width:(.*?)"></span>',re.S)#评价星级
        rated_star = re.findall(pattern8, data)
    except:
        rated_star = [' ']
    try:
        pattern3 = re.compile('<span class="time">(.*?)</span>', re.S)  # 评价日期
        rated_star_date = re.findall(pattern3, data)
    except:
        rated_star_date = [' ']

    shop_id_list=[]
    for i in user_content:
     shop_id_list.append(shop_id[0])

    items = zip(shop_id_list,user_name, user_content, rated_star, rated_star_date)
    user_content_list=list(items)
    # 写入文件
    try:
        with open('C:/Users/Administrator/Desktop/shop_content.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in list(user_content_list):
             spamwriter.writerow(i)
        time.sleep(10)
    except:
        with open('C:/Users/Administrator/Desktop/shop_content.txt', 'a', encoding='utf-8') as f:
            # spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for v1, v2, v3, v4, v5 in user_content_list:
                f.write("%s,%s,%s,%s,%s" % (v1, v2, v3, v4, v5))
                f.write('\n')

#拿到商铺同类等信息
#def shop_similar(url):
    try:
        pattern = re.compile('<h5><a data-mttcode="Aresys.Bshop.Cother.Drightside" target="_blank" class="title" href=.*?>(.*?)</a>')#同类团购
        similar_groupon = re.findall(pattern, data)
    except:
        similar_groupon=[' ']

    try:
        pattern1 = re.compile('<a data-mttcode="Aresys.Bshop.Cother.Drightside" target="_blank" class="shop-name" title=".*?>(.*?)</a>')  # 同类商家
        similar_shop = re.findall(pattern1, data)
    except:
        similar_shop=[' ']

    len1 = len(similar_groupon)
    len2 = len(similar_shop)

    if len1 > len2:
        print(1)
        for i in range(len1 - len2):
            similar_shop.append(' ')
    elif len1 < len2:
        for i in range(len2 - len1):
            similar_groupon.append(' ')


    shop_id_l = []
    for i in similar_groupon:
        shop_id_l.append(shop_id[0])

    items = zip(shop_id_l , similar_groupon , similar_shop)
    similar_list=list(items)
    # 写入文件
    try:
        with open('C:/Users/Administrator/Desktop/shop_similar.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in list(similar_list):
                spamwriter.writerow(i)
        time.sleep(10)
    except:
        with open('C:/Users/Administrator/Desktop/shop_similar.txt', 'a', encoding='utf-8') as f:
            # spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for v1, v2, v3 in similar_list:
                f.write("%s,%s,%s" % (v1, v2, v3))
                f.write('\n')

    print("拿取成功")
    success_address=[]
    with open('C:/Users/Administrator/Desktop/shop_success.txt', 'r') as f:
        for line in f:
            success_address.append(line.replace('\n',''))
    if url not in success_address:
        with open('C:/Users/Administrator/Desktop/shop_success.txt', 'a') as csvfile:
            #spamwriter = csv.writer(csvfile, delimiter='', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #spamwriter.writerow(url)
            csvfile.write(url+'\n')

'''
with open('C:/Users/Administrator/Desktop/food_first.csv', 'w', newline='') as csvfile:
    pass
with open('C:/Users/Administrator/Desktop/shop_first.txt', 'a', encoding='utf-8') as f:
    pass
for i in range(1,10):
    url="http://cd.meituan.com/category/meishi/all/page"+str(9)
    try:
         food_first_list=meituan_frist(url)
         time.sleep(10)
         try:
             with open('C:/Users/Administrator/Desktop/food_first.csv', 'a', newline='') as csvfile:
                 spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                 for item in food_first_list:
                     spamwriter.writerow(item)
         except:
             with open('C:/Users/Administrator/Desktop/food_first.txt', 'a', encoding='utf-8') as f:
                 for v1, v2, v3, v4, v5 in food_first_list:
                     f.write("%s,%s,%s,%s,%s" % (v1, v2, v3, v4, v5))
                     f.write('\n')
    except Exception as err:
         print('报错了:'+url)
         print(err)
'''



shop_web=[]
with open('C:/Users/Administrator/Desktop/test1.csv', newline='',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        shop_web.append(row[0])
print(shop_web)
sum=len(open('C:/Users/Administrator/Desktop/test1.csv').readlines())

#with open('C:/Users/Administrator/Desktop/shop.csv', 'w', newline='') as csvfile:
#    pass
#with open('C:/Users/Administrator/Desktop/shop_content.csv', 'w', newline='') as csvfile:
#    pass
#with open('C:/Users/Administrator/Desktop/shop_similar.csv', 'w', newline='') as csvfile:
#    pass
#with open('C:/Users/Administrator/Desktop/shop_success.txt', 'w', newline='') as csvfile:
#    pass
success = 0
while success<sum:
    for url in shop_web:
        print('总数：%s,成功数:%s' % (sum, success))
        success_address = []
        with open('C:/Users/Administrator/Desktop/shop_success.txt', 'r') as f:
            for line in f:
                success_address.append(line.replace('\n',''))
        if url not in success_address:
               #time.sleep(10)
               try:
                 shop_info(url)
                 time.sleep(10)
               except Exception as err:
                print('报错了:'+url)
                print(err)
                continue
        success = len(open('C:/Users/Administrator/Desktop/shop_success.txt').readlines())
        #time.sleep(10)


#print(time.ctime())
#items=meituan_frist('http://cd.meituan.com/category/meishi?mtt=1.index%2Ffloornew.nc.1.issbkisk')
#with open('C:/Users/Administrator/Desktop/test1.csv','w', newline='') as csvfile:
#    pass
#with open('C:/Users/Administrator/Desktop/test1.csv','a', newline='') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for item in list(items):
#      spamwriter.writerow(item)
#print(time.ctime())

#for url in shop:
#    try:
#     #shop_similar(url)
#     time.sleep(1)
#    except:
#      print('各种报错')
#      continue
#shop_similar('http://cd.meituan.com/shop/60120047')



#for i in shop:
# shop_info(i)
#with open('C:/Users/Administrator/Desktop/test.csv', 'w', newline='') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for i in items6:
#       spamwriter.writerow(i);


