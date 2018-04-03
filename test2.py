# coding=utf-8

"""
Created on 2016-02-22 @author: Eastmount

功能: 爬取新浪微博用户的信息
信息：用户ID 用户名 粉丝数 关注数 微博数 微博内容
网址：http://weibo.cn/ 数据量更小 相对http://weibo.com/

"""
import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import math


# 先调用无界面浏览器PhantomJS或Firefox
# driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")
chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
#driver = webdriver.Chrome(chrome_driver)
driver = webdriver.Chrome()
wait = ui.WebDriverWait(driver, 10)

file='sina'
path='C:/Users/Administrator/Desktop/sina/'
day_date=str(time.strftime("%Y-%m-%d",time.localtime()))
dayfile='day_constantly'

#写入文件
def GetFile(data,title,type):
    # 没有文件的话生成文件
    if not os.path.exists( '%s%s_%s.txt' %(path,file,title) ):
        with open(file, 'w', encoding='utf-8') as f:
            pass

    if type==1:
        with open('%s%s_%s.txt' %(path,file,title), 'a', encoding='utf-8') as f:
           f.write(data)
           f.write('\n')


# ********************************************************************************
#                  第一步: 登陆weibo.cn 获取新浪微博的cookie
#        该方法针对weibo.cn有效(明文形式传输数据) weibo.com见学弟设置POST和Header方法
#                LoginWeibo(username, password) 参数用户名 密码
#                             验证码暂停时间手动输入
# ********************************************************************************

def LoginWeibo(username, password):
    try:
        # **********************************************************************
        # 直接访问driver.get("http://weibo.cn/5824697471")会跳转到登陆页面 用户id
        #
        # 用户名<input name="mobile" size="30" value="" type="text"></input>
        # 密码 "password_4903" 中数字会变动,故采用绝对路径方法,否则不能定位到元素
        #
        # 勾选记住登录状态check默认是保留 故注释掉该代码 不保留Cookie 则'expiry'=None
        # **********************************************************************

        # 输入用户名/密码登录
        print( u'准备登陆Weibo.cn网站...')
        driver.get("https://login.sina.com.cn/signup/signin.php")
        time.sleep(10)
        elem_user = driver.find_element_by_name("username")
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_xpath('//*[@id="password"]')
        elem_pwd.send_keys(password)  # 密码
        # elem_rem = driver.find_element_by_name("remember")
        # elem_rem.click()             #记住登录状态

        # 重点: 暂停时间输入验证码
        # pause(millisenconds)
        time.sleep(5)

        elem_sub = driver.find_element_by_xpath('//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input')
        elem_sub.click()  # 点击登陆
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        # 获取Coockie 推荐 http://www.cnblogs.com/fnng/p/3269450.html
        print(driver.current_url)
        print(driver.get_cookies() ) # 获得cookie信息 dict存储
        print(u'输出Cookie键值对信息:')
        for cookie in driver.get_cookies():
            # print cookie
            for key in cookie:
                print(key, cookie[key])

                # driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print(u'登陆成功...')
    except Exception as e:
        print("Error: ", e)
    finally:
        print(u'End LoginWeibo!\n\n')

    return driver

def get_data(driver,url,title):
    driver.get(url)
    time.sleep(10)
    data=driver.page_source
    soup = BeautifulSoup(data, "html.parser")
    regex_num = r'<span>找到(.*?)条结果'
    try:
       result_num = re.findall(regex_num, data)[0]
    except:
       result_num = 20
    sum_page=math.ceil(int(result_num)/20)
    if sum_page>50:
        sum_page=50
    for page in range(1,sum_page+1):
        url = 'http://s.weibo.com%s&page=%d' % (follows_url,page)
        driver.get(url)
        time.sleep(20)
        for sel in soup.find_all('div',class_="feed_content wbcon"):
            user_name = sel.find('a').next.replace('\n','').replace(' ','').replace('\t','').strip()
            #print(user_name)
            user_id = sel.find('a').get('href').replace('\n','').replace(' ','')
            #print(user_id)
            content = sel.find('p',class_='comment_txt').text.replace('\n','').replace(' ','').replace('\t','').strip()
            #print(content)
            data='%s[}%s[}%s' %(user_name,user_id,content)
            GetFile(data,title,1)
        with open('%s%s_%s.txt' % (path, dayfile, day_date), 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')

def get_url(driver,url):
    driver.get(url)
    time.sleep(5)
    data=driver.page_source
    soup = BeautifulSoup(data,"html.parser")
    follows_list=[]
    for sel in soup.find_all('div',class_='pl_Sranklist02')[0].find_all('tr'):
        follows_url=sel.find('p',class_='star_name').find('a').get('href')
        title = sel.find('p', class_='star_name').find('a').next.replace(' ','')
        content='%s[}%s' %(follows_url,title)
        follows_list.append(content)
        print(content)
    return follows_list


# *******************************************************************************
#                                程序入口 预先调用
# *******************************************************************************

if __name__ == '__main__':

    # 定义变量
    username = '17761217812'  # 输入你的用户名
    password = 'he3523227'  # 输入你的密码
    #user_id = 'guangxianliuyan'  # 用户id url+id访问个人

    # 操作函数
    url='http://s.weibo.com/top/summary?cate=homepage'
    driver=LoginWeibo(username, password)  # 登陆微博
    url_list=get_url(driver, url)
    #query = '%25E8%2599%259A%25E6%258B%259F%25E7%258E%25B0%25E5%25AE%259E'  # 虚拟现实
    start_urls = []
    title_list=[]
    with open('%s%s_%s.txt' % (path,dayfile, day_date), 'r', encoding='utf-8') as f:
        for line in f:
           title_list.append(line.replace('\n',''))
    print(title_list)
    for follows_url in url_list:
            url = 'http://s.weibo.com%s&page=%d' % (follows_url.split('[}')[0], 1)
            time.sleep(10)
            print(follows_url.split('[}')[1])
            if follows_url.split('[}')[1] not in title_list:
                get_data(driver, url,follows_url.split('[}')[1])
    driver.quit()
    #&Refer=index