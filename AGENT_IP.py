import urllib.request
import urllib
from bs4 import BeautifulSoup
import pexpect
import re
import os

class IPItem:
    def __init__(self):
        self.ip = ''    # IP
        self.port = ''  # Port
        self.anonymous = ''  # 匿名度
        self.tpye = ''  #类型:http; https
        self.address='' #位置
        self.speed = -1 #速度

#爬取匿名的代理IP
def parse(url):
    ip_list = []
    try:
        page = urllib.request.urlopen(url)
        data =  page.read()
        soup = BeautifulSoup(data,"html.parser")
        #print(soup.get_text())
        body_data = soup.find('tbody')
        res_list = body_data.find_all('tr')
        for res in res_list:
            each_data = res.find_all('td')
            if len(each_data) > 3 and not 'IP' in each_data[0].get_text() and '.' in each_data[0].get_text() and '透明' not in each_data[2].get_text():
                ip='%s:%s'%(each_data[0].get_text().strip(),each_data[1].get_text().strip())
                ip_list.append(ip)
        return ip_list
                #item = IPItem()
                #item.ip = each_data[0].get_text().strip()
                #item.port = each_data[1].get_text().strip()
                #item.anonymous = each_data[2].get_text().strip()
                #item.tpye = each_data[3].get_text().strip()
                #item.address = each_data[5].get_text().strip()
                #item.speed = each_data[6].get_text().strip()
                #ip_items.append(item)
    except Exception as e:
        print(e)

#测试代理IP
def test_ip_speed(ip_list):
    tmp_items = []
    for item in ip_list:
        ip=item.split(':')[0]
        result = os.system('ping %s' % ip)
        if result:
            print('服务器%s ping fail' % ip)
        else:
            print('服务器%s ping ok' % ip)
            tmp_items.append(item)
    return tmp_items


ip_may_list=[]
list=[]
list_items=[]

for i in range(11):
 url='http://www.kuaidaili.com/proxylist/'+str(i)
 list_items=parse(url)
 for ip in list_items:
     list.append(ip)

ip_may_list=test_ip_speed(list)
print(ip_may_list)
