import re
import csv
import random
import urllib.request
import http.cookiejar
import urllib.parse
import time
import socket
from collections import deque
from openpyxl import Workbook
from openpyxl import load_workbook
from  openpyxl.workbook  import  Workbook
from openpyxl.utils import get_column_letter

#模拟浏览器,影藏IP
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):

    iplist = ['60.194.100.51:80', '61.162.223.41:9797', '61.174.10.22:8080']
    proxy_support = urllib.request.ProxyHandler({'http': random.choice(iplist)})
    opener = urllib.request.build_opener(proxy_support)
    cj = http.cookiejar.CookieJar()
    #opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

#爬取美团美食首页
def meituan_frist(url):
        url = url
        html = reptiles(url)
        pattern  = re.compile( '<img class="J-webp" src="(.*?.jpg).*?"')
        pattern1 = re.compile( '<a class="link f3 J-mtad-link" href="(.*?)"')
        pattern2 = re.compile( '<a class="link f3 J-mtad-link" .*?>(.*?)</a>')
        pattern3 = re.compile( '<span class="num">(.*?)</span>')
        pattern4 = re.compile( '<span class="price">¥(.*?)</span>')
        pattern5 = re.compile( '<span class="prefix">.*?</span>(.*?)</span>')

        #f = open("C:/Users/Administrator/Desktop/foo1.txt", "r",encoding='utf-8')
        #html=f.read()
        #f.close()
        items = re.findall(pattern, html) #图片地址
        items1 = re.findall(pattern1, html)#店铺地址
        items2 = re.findall(pattern2, html)#店铺名称
        items3 = re.findall(pattern3, html)#评价人数
        items4 = re.findall(pattern4, html)#人均价位
        items5 = re.findall(pattern5, html)#最低价位

        # 下载图片
        for i in items:
            filename = i.split('/')[-1]
            print('aa=' + i)
            conn = urllib.request.urlopen(i)
            img = conn.read()
            with open('D:/photo/%s' % filename, 'wb') as f:
                f.write(img)

        #for item in items:
        #    print(item)
        #print('######################################################################################')
        #for item1 in items1:
        #    print(item1)
        print('######################################################################################')
        for i in range(0,len(items)):
            items[i]='D:/photo/%s' % items[i].split('/')[-1]
        print('######################################################################################')
        for i in range(0,len(items3)):
             items3[i]='%s人评价' % items3[i]
        print('######################################################################################')
        for i in range(0, len(items4)):
                items4[i]='人均%s元' % str(items4[i])
        print('######################################################################################')
        for i in range(0, len(items5)):
             items5[i]='%s元起' % (items5[i])
        print('######################################################################################')



        items6=zip(items1,items,items2,items3,items4,items5)
        return items6

#进入店铺里爬出店铺信息
def shop_info(url):
    url=url
    data=reptiles(url)
    pattern = re.compile('<span class="title">(.*?)</span>')#店铺名称
    items=re.findall(pattern,data)
    items.remove(items[1])

    pattern1 = re.compile('<span class="geo">(.*?)</span>')#店铺地址
    items1 = re.findall(pattern1, data)
    items1.remove(items1[1])

    pattern2 = re.compile('<p class=under-title>(.*?)</p>')#店铺电话
    items2 = re.findall(pattern2, data)

    pattern3 = re.compile('<strong>(.*?)</strong>')#店铺分数
    items3 = re.findall(pattern3, data)

    pattern4 = re.compile('<a href=".*?" target=_blank class=tag>(.*?)</a>')#店铺类型
    items4 = re.findall(pattern4, data)

    pattern5 = re.compile('<div>消费人数 <span class="num">(.*?)</span>')#总消费人数
    items5 = re.findall(pattern5, data)

    pattern6 = re.compile('<span class="field-title">营业时间：</span>(.*?)<div>')  # 营业时间
    items6 = re.findall(pattern6, data)

    pattern7 = re.compile('<span class="inline-item">\s*([\s\S]*?)\s*</span>')  # 营业时间
    items7 = re.findall(pattern7, data)
    items7 = ','.join(items7)

    pattern8 = re.compile('<span class="inline-item">\s*([\s\S]*?)\s*</span>')  # 门店介绍
    items8 = re.findall(pattern8, data)


    items6 = zip(items, items1, items2, items3, items4, items5)
    return items6


#拿到用户评论等信息
def user_content(url):
    url = url
    data = reptiles(url)
    pattern = re.compile('<span class="name vip_level_high">(.*?)</span>')#评论用户用户名
    items = re.findall(pattern, data)

    pattern1 = re.compile('<p\sclass="content".*?>\s*(?:<a.*?</a>)?\n(.*?)</p>',re.S)#用户评论
    #pattern1 = re.compile('<p class="content">(?:.*?<a.*?><strong.*?</s.*?</a>)?(.*?)</p>',re.S)
    items1 = re.findall(pattern1, data)
    for i in range(0, len(items1)):
       items1[i] = items1[i].strip()

    pattern8 = re.compile('<div class="rate-status">.*?<span class="common-rating"><span class="rate-stars" style="width:(.*?)"></span>',re.S)#评价星级
    items2 = re.findall(pattern8, data)

    pattern3 = re.compile('<span class="time">(.*?)</span>', re.S)  # 评价日期
    items3 = re.findall(pattern3, data)

    pattern4 = re.compile('<span class="title">(.*?)</span>')  # 店铺名称
    items4 = re.findall(pattern4, data)
    items4.remove(items4[1])
    for i in items3:
     items4.append(items4[0])

    items5 = zip(items4,items, items1, items2, items3)
    return items5

#拿到商铺同类等信息
def shop_similar(url):
    url = url
    data = reptiles(url)
    if data==0:
      print('报错了')
      return 0
    pattern = re.compile('<h5><a data-mttcode="Aresys.Bshop.Cother.Drightside" target="_blank" class="title" href=.*?>(.*?)</a>')#同类团购
    items = re.findall(pattern, data)
    print(items)

    pattern1 = re.compile('<a data-mttcode="Aresys.Bshop.Cother.Drightside" target="_blank" class="shop-name" title=".*?>(.*?)</a>')  # 同类商家
    items1 = re.findall(pattern1, data)

    pattern2 = re.compile('<span class="title">(.*?)</span>')  # 店铺名称
    items2 = re.findall(pattern2, data)
    items2.remove(items2[1])
    for i in items1:
     items2.append(items2[0])

    items3 = zip(items2 , items , items1)
    return items3


def reptiles(url):
    # 入口页面, 可以换成别的
    visited = set()
    queue = deque()
    cnt=0
    queue.append(url)
    socket.setdefaulttimeout(5)
    while queue:
        url = queue.popleft()  # 队首元素出队
        visited |= {url}  # 标记为已访问

        print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
        cnt += 1
        oper = makeMyOpener()
        urlop = oper.open(url,timeout=100)
        #urlop = urllib.request.urlopen(url)
        if 'html' not in urlop.getheader('Content-Type'):
            continue

        # 避免程序异常中止, 用try..catch处理异常
        try:
            data = urlop.read().decode('utf-8')
            print('拿到数据')
            return data
        except:
            print('没有拿到')
            return 0



shop=[]
with open('C:/Users/Administrator/Desktop/test.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        shop.append(row[1])



#print(time.ctime())
#items=meituan_frist('http://cd.meituan.com/category/meishi?mtt=1.index%2Ffloornew.nc.1.issbkisk')
#with open('C:/Users/Administrator/Desktop/test1.csv','w', newline='') as csvfile:
#    pass
#with open('C:/Users/Administrator/Desktop/test1.csv','a', newline='') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for item in list(items):
#      spamwriter.writerow(item)
#print(time.ctime())

for url in shop:
    try:
     shop_similar(url)
     time.sleep(1)
    except:
      print('各种报错')
      continue
#shop_similar('http://cd.meituan.com/shop/60120047')



#for i in shop:
# shop_info(i)
#with open('C:/Users/Administrator/Desktop/test.csv', 'w', newline='') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for i in items6:
#       spamwriter.writerow(i);


