# -*- coding: utf-8 -*-
import re
import time
from BeautifulSoup import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import math
import datetime
import os
import json
import pymongo

MONGOD_HOST = '127.0.0.1'
MONGOD_PORT = 27017
MONGOD_DB = 'weixin_public'
MONGOD_COLLECTION = 'zhongchuanzhonggong'



def _default_mongo(host=MONGOD_HOST, port=MONGOD_PORT, usedb=MONGOD_DB):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=False, w=1)
    # db = connection.admin
    # db.authenticate('root', 'root')
    db = getattr(connection, usedb)
    return db


#scrapy recent data
class Spider(object):
    def __init__(self):
        HOST_URL = "http://mp.weixin.qq.com"
        self.db = _default_mongo()
        self.spiders = []
        self.client = webdriver.Firefox()
        print ('start')
        weixin_public_url = ['https://www.baidu.com/', \
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1466315714&ver=1&signature=TEyVYDbnA7uiquirD26XSD5S6PbEA0a*ZVm3RvSvVBb7vgy7BBRr8vwmhx10kienEVRzxcaXYMH0I0Yq3B*wCA==', \
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1466315735&ver=1&signature=DpislL1L0olhEXB77suLNIxEESxa34yhqchrfe*edc39rQYz6vLZAEy3LK4tp3aWrWgs9YK4pgT8i7zA97a43Q==', \
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1466315748&ver=1&signature=*D2G2aZ3gO6sDu-VVYd5YKvYjkmOpxv12WGoirdSQavoGVgTrnmwkSkL9nZEocDe-nEH-UzrIuZy5fI9YzScOQ==', \
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1466315765&ver=1&signature=LJnINzomw8Pl5TIv57i0BC31n6flTPqyq5AE-OeSsF0nt3oUcKSYUycxL-2ljNPtplMdwnnWiD27w*-hNd4GXQ==', \
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1466315780&ver=1&signature=AZJIcqSz8DTnWXu6hwVOn89pNOf*JFKVA0Oohf21GxtcLngBhKvtN1FEPG5xmabrc*WDULozJgOgCccBaxod6w==']
        # 中船重工
        # 中国船舶报
        # 《贸易风》海事周报
        # seawaymaritime
        # 中船重工经济研究中心
        count = 0 
        for i in range(0,len(weixin_public_url)):
            print (weixin_public_url[i])
            count = count + 1          
            self.client.get(weixin_public_url[i])
            # self.client.maximize_window()
            time.sleep(5)
            if i == 0:
                pass
            elif i == 1:
                post_source_name = "中船重工"
            elif i == 2:
                post_source_name = "中国船舶报"
            elif i == 3:
                post_source_name = "《贸易风》海事周报"
            elif i == 4:
                post_source_name = "seawaymaritime"
            else:
                post_source_name = "中船重工经济研究中心"

            # more_c = 1
            # while more_c:
            #      try:
            #         print '点击查看更多'
            #         more_click = self.client.find_element_by_link_text('查看更多')
            #         more_click.click()
            #         time.sleep(2)
            #         more_c = 1
            #      except:
            #         more_c = 0
            count = 0
            soup = BeautifulSoup(self.client.page_source)
            msg_card_list = soup.findAll("div", {"class": "weui_msg_card"})
            # print len(msg_card_list)
            for msg_card in msg_card_list:
                weui_media_box = msg_card.findAll("div", {"class": "weui_media_box appmsg"})
                # print len(weui_media_box)
                for media_box in weui_media_box:
                    count = count + 1
                    weui_media_hd = media_box.find("span", {"class": "weui_media_hd"})
                    # post_url = weui_media_hd.get("hrefs")
                    post_img = weui_media_hd.get("style")
                    timestamp = int(weui_media_hd.get("data-t"))/1000

                    weui_media_bd = media_box.find("div", {"class": "weui_media_bd"})
                    weui_media_bd_h4 = weui_media_bd.find("h4")
                    post_url = weui_media_bd_h4.get("hrefs")
                    if weui_media_bd_h4.find("span", {"class": "icon_original_tag"}):
                        weui_media_bd_h4_split = str(weui_media_bd_h4).split(">")
                        post_title_split = weui_media_bd_h4_split[3].split("<")
                        post_title = post_title_split[0].strip()
                    else:
                        weui_media_bd_h4_split = str(weui_media_bd_h4).split(">")
                        post_title_split = weui_media_bd_h4_split[1].split("<")
                        post_title = post_title_split[0].strip()
                    # print post_title                   
                    post_url = HOST_URL + str(post_url)

                    weui_media_desc = weui_media_bd.find("p", {"class": "weui_media_desc"})
                    weui_media_desc_split = str(weui_media_desc).split(">")
                    post_summary_split = weui_media_desc_split[1].split("<")
                    post_summary = post_summary_split[0].strip()
                    # print post_summary
                    date = self.ts2date(timestamp)
                    datetime = self.ts2datetime(timestamp)
                    # print post_url,post_id,post_img,datetime,post_summary,post_title
                    item = {'_id': post_url,'post_img': post_img, 'post_title': post_title, 'post_url': post_url, \
                            'post_summary': post_summary, 'post_source_name': post_source_name, \
                            'timestamp': timestamp, 'date': date, 'datetime': datetime}
                    self.process_item(item)
            print(count)
                    # print item
        print ('end')
        self.client.close()
            
    def process_item(self,item):
        if self.db[MONGOD_COLLECTION].find({"post_url":item["post_url"]}).count():
            self.update_item(item)
        else:
            try:
                item["first_in"] = time.time()
                item["last_modify"] = item["first_in"]
                self.db[MONGOD_COLLECTION].insert(item)
            except:
                self.update_item(item)


    def update_item(self,item):
        item['last_modify'] = time.time()
        updates_modifier = {'$set':item}
        self.db[MONGOD_COLLECTION].update({'post_url':item['post_url']},updates_modifier)

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def ts2datetime(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def main():
    
    s = Spider()
        
if __name__ == '__main__':
    main()

