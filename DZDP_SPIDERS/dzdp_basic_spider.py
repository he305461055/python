from selenium import webdriver
import random
from bs4 import BeautifulSoup
import time
import  traceback
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
'''
def open_socket_web():
    #'124.240.187.84','139.196.108.68','122.114.36.13','182.90.252.10',
         IP=['122.96.95.70:32 ']
         PROXY = random.choice(IP)#"122.96.59.106:81" # IP:PORT or HOST:PORT
         chrome_options = webdriver.ChromeOptions()
         chrome_options.add_argument('--proxy-server=%s' % PROXY)
         driver = webdriver.Chrome(chrome_options=chrome_options)
         #driver = webdriver.Chrome()
         driver.get('http://www.dianping.com/shop/65583778')

open_socket_web()
'''
log_dir='C:/Users/Administrator/Desktop/DZDP_BASIC/test/log/'
img_dir='D:/photo/dzdp/test/'
config_dir='E:/python/DZDP_SPIDERS/config/'
data_dir='C:/Users/Administrator/Desktop/DZDP_BASIC/test/'
channel_name='DZDP'
contentfilename='shopping_user_content'
detailfilename='shopping_detail'
webaddressfilename='dzdp_web_address'
successfilename='dzdp_success_list'
basicfilename='dzdp_basic_list'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if_start=0

#记录步骤
def MARKING(filename,value,type):
    file='E:/python/DZDP_SPIDERS/config/%s.txt' %filename
    if type==1:
        with open(file, 'w', encoding='utf-8') as f:
            pass
        with open(file, 'a', encoding='utf-8') as f:
            f.write(str(value))

    if type==2:
        with open(file, 'r', encoding='utf-8') as f:
            startstep=f.read()
        return int(startstep)

#写入文件
def GetFile(filename,data,type,count):
    # 没有文件的话生成文件
    if os.path.exists(r'%s%s_variable.txt' %(config_dir,filename)):
        pass
    else:
        with open('%s%s_variable.txt' %(config_dir,filename), 'w', encoding='utf-8') as f:
            pass

    variable = len(open('%s%s_variable.txt' %(config_dir,filename),encoding='utf-8').readlines())
    file='%s%s_%s_%d.txt' % (data_dir,channel_name, filename,variable)
    # 没有文件的话生成文件
    if os.path.exists(r'%s' % file):
        pass
    else:
        with open(file, 'w', encoding='utf-8') as f:
            pass

    if type==1:
        with open(file, 'a', encoding='utf-8') as f:
           f.write(data)
           f.write('\n')
    if type==3:
        sum = -1
        for sum, line in enumerate(open(r"%s" % file, 'rU', encoding='utf-8')):
            pass
        sum += 1
        if sum<count:
            with open(file, 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')
        else:
            with open('%s%s_variable.txt' %(config_dir,filename), 'a', encoding='utf-8') as f:
                f.write('global')
                f.write('\n')
            variable = len(open('%s%s_variable.txt' %(config_dir,filename),encoding='utf-8').readlines())
            file = '%s%s_%s_%d.txt' % (data_dir,channel_name, filename, variable)
            with open(file, 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')

#写入日志
def GetLog(name,data):
    datetime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    date=time.strftime("%Y-%m-%d",time.localtime())
    data='[%s]%s:::::%s' %(str(datetime),str(date),data)
    file = '%s%s_%s_%s.txt' % (log_dir,name, 'LOG',str(date))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

def GET_SOUP(driver):
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")
    return soup

##点击区域
def CLICK_REGION(driver,soup,name,filename,small_type):
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="J_nav_tabs"]/a[2]/span').click()
    soup=GET_SOUP(driver)
    big_region_list = soup.find('div', attrs={"id": "region-nav"}).find_all('a')  # 获取地区大类
    get_more = driver.find_element_by_xpath('//*[@id="region-nav"]/a[last()]').text  # 拿取列表最后一个值是否为更多
    if get_more == '更多':
        mark_step=len(big_region_list)
        driver.find_element_by_xpath('//*[@id="region-nav"]/a[last()]').click()# 点击更多按钮
        soup = GET_SOUP(driver)
        big_region_list = soup.find('div', attrs={"id": "region-nav"}).find_all('a')  # 获取地区大类
        big_step = len(big_region_list)
    else:
        mark_step=0
        big_step = len(big_region_list) + 1

    startstep=MARKING('big_region','',2)

    for i in range(startstep,big_step):
        time.sleep(5)
        MARKING('big_region', i, 1)
        big_region = big_region_list[i-1].find('span').next
        button = '//*[@id="region-nav"]//span[text()="' + big_region + '"]'
        if big_region == '天台山':
            print('有天台山跳过')
            continue
        if i==15 and get_more == '更多':
            try:
              driver.find_element_by_xpath('//*[@id="region-nav"]/a[last()]').click()  # 点击更多按钮
            except:
               pass

        try:
            #big_region = soup.find('div',attrs={'id':'region-nav'}).find_all('a')[i-1].text
            driver.find_element_by_xpath(button).click()  # 点击地区大类
            print('################################地区大类：%s' % big_region)
            time.sleep(5)
        except:
            try:
              driver.find_element_by_xpath('//div[@class="nav-category J_filter_category"]/a[1]/span').click()  # 点击不限
              time.sleep(5)
              print('点击地点不限')
              if i == 15 and get_more == '更多':
                  try:
                      driver.find_element_by_xpath('//*[@id="region-nav"]/a[last()]').click()  # 点击更多按钮
                      soup = GET_SOUP(driver)
                  except:
                      pass
              driver.find_element_by_xpath(button).click()  # 点击地区大类
              print('################################地区大类：%s' % big_region)
              time.sleep(5)
            except:
               driver.back()  #有可能遇到页面没有数据的情况，后退一下
               GetLog('dzdp', '这页没有数据回退一下，请查看是否正确')
               continue

        GetLog('dzdp', '################################地区大类：%s' % big_region)

        time.sleep(1)
        soup=GET_SOUP(driver)

        #拿取小类列表是否存在
        try:
           small_region_list = soup.find("div", attrs={'id': 'region-nav-sub'}).find_all('a')  # 拿取地区小类
        except:
            soup = GET_SOUP(driver)
            small_region = ' '
            print('2开始执行函数')
            try:
              SHOP_BASIS_INFO(name, soup, filename,small_type,big_region,small_region)
            except:
                GetLog('dzdp', '[ERROR:][ERROR:][ERROR:]%s_%s_%s错误' % (small_type, big_region, small_region))
                print('%s_%s_%s错误' % (small_type, big_region, small_region))

            try:
               CLICK_NEXT(driver,soup,name,filename,big_region,small_region)
            except Exception as e:
                print('在2位置')
                print(e)
                continue


        get_snall_more = driver.find_element_by_xpath('//*[@id="region-nav-sub"]/a[last()]').text  # 拿取列表最后一个值是否为更多
        if get_snall_more == '更多':
            driver.find_element_by_xpath('//*[@id="region-nav-sub"]/a[last()]').click()# 点击更多按钮
            time.sleep(1)
            soup = GET_SOUP(driver)
            small_region_list = soup.find("div", attrs={'id': 'region-nav-sub'}).find_all('a')  # 拿取地区小类
            small_step = len(small_region_list)
        else:
            small_step = len(small_region_list) + 1

        start=MARKING('small_region', '', 2)

        for j in range(start, small_step):
            time.sleep(5)
            small_region = small_region_list[j-1].find('span').next
            if j == 15  and get_snall_more == '更多':
                try:
                  driver.find_element_by_xpath('//div[@id="region-nav-sub"]/a[last()]').click()  # 点击更多按钮
                  soup=GET_SOUP(driver)
                except:
                  pass

            button = '//*[@id="region-nav-sub"]//span[text()="' + small_region + '"]'

            try:
                driver.find_element_by_xpath(button).click()  # 点击地区小类
                time.sleep(5)
                print('#########地区小类：%s' % small_region)
            except:
                driver.refresh()
                driver.find_element_by_xpath('//*[@id="region-nav-sub"]//span[text()="不限"]').click() #点击不限
                time.sleep(5)
                if j == 15 and get_snall_more == '更多':
                    try:
                        driver.find_element_by_xpath('//*[@id="region-nav-sub"]/a[last()]').click()  # 点击更多按钮
                        time.sleep(1)
                    except:
                        pass
                try:
                    driver.find_element_by_xpath(button).click()# 点击地区小类
                    time.sleep(5)
                except NoSuchElementException as e:
                    print('can not find the button')
                print('#########地区小类：%s' % small_region)



            MARKING('small_region', j, 1)

            soup = GET_SOUP(driver)
            GetLog('dzdp', '#########地区小类：%s' %small_region)
            print('####1开始执行函数')
            try:
              SHOP_BASIS_INFO(name, soup, filename,small_type,big_region,small_region)
            except:
                GetLog('dzdp', '[ERROR:][ERROR:][ERROR:]%s_%s_%s错误' % (small_type, big_region, small_region))
                print('%s_%s_%s错误' % (small_type, big_region, small_region))
                traceback.print_exc()
                driver.back()
                time.sleep(5)
                continue

            try:
              CLICK_NEXT(driver,soup,name,filename,small_type,big_region,small_region)

              small_regoin_temp = MARKING('small_region', '', 2)  #当小区域循环执行完的时候把开始步数重新设置为2
              if small_regoin_temp == small_step-1:
                  print('开始小地域重新设置为2')
                  MARKING('small_region', 2, 1)

              big_regoin_temp = MARKING('big_region', '', 2)  # 当大区域循环执行完的时候把开始步数重新设置为1
              if big_regoin_temp == big_step - 1:
                  print('开始大地域重新设置为1')
                  MARKING('big_region', 1, 1)

            except Exception as e:
                print('在1位置')
                traceback.print_exc()
                driver.refresh()
                time.sleep(5)
                try:
                   driver.refresh()
                   time.sleep(5)
                   soup=GET_SOUP(driver)
                   CLICK_NEXT(driver, soup, name, filename, small_type, big_region, small_region)

                   small_regoin_temp = MARKING('small_region', '', 2)  # 当小区域循环执行完的时候把开始步数重新设置为2
                   if  small_regoin_temp == small_step-1 :
                       print('开始小地域重新设置为2')
                       MARKING('small_region', 2, 1)

                   big_regoin_temp = MARKING('big_region', '', 2)  # 当大区域循环执行完的时候把开始步数重新设置为1
                   if big_regoin_temp == big_step - 1:
                       print('开始大地域重新设置为1')
                       MARKING('big_region', 1, 1)

                except Exception as e:
                    print('特殊异常：')
                    traceback.print_exc()


##点击分类类型
def CLICK_TYPE(driver,soup,name,filename):
    type_list = soup.find('div', attrs={'id': "classfy"}).find_all('a')  # 拿取分类

    startstep=MARKING('big_type', '', 2)#读取上次程序中断后停留的地方

    for k in range(startstep, len(type_list)):
        #每次循环一次重置一下分类和地区，因为可能与最开始看到的顺序不一致
        time.sleep(5)
        driver.find_element_by_xpath('//div[@class="nav-category J_filter_category"]/a[1]/span').click()  # 点击分类不限
        time.sleep(5)
        driver.find_element_by_xpath('//div[@class="nav-category nav-tabs J_filter_region"]/a[1]/span').click()  # 点击地区不限
        time.sleep(5)

        if k>=15:
            driver.find_element_by_xpath('//*[@id="classfy"]/a[last()]').click()  # 点击更多

        big_type = type_list[k-1].find('span').next  # 大类名称

        button = '//*[@id="classfy"]//span[text()="'+str(big_type)+'"]'
        try:
           driver.find_element_by_xpath(button).click()  # 点击分类
           time.sleep(3)
           print('######################################################################分类大类：%s' % big_type)
        except:
            driver.refresh()
            time.sleep(5)
            if k == 15:
                driver.find_element_by_xpath('//*[@id="classfy"]/a[last()]').click()  # 点击更多
            driver.find_element_by_xpath(button).click()  # 点击分类
            time.sleep(3)
            print('######################################################################分类大类：%s' % big_type)

        MARKING('big_type', k, 1)

        # 重新获取页面，拿取分类小类
        soup = GET_SOUP(driver)

        GetLog('dzdp','######################################################################分类大类：%s' %big_type)

        #拿取小类列表是否存在
        try:
           type_small_list = soup.find('div', attrs={'id': "classfy-sub"}).find_all('a')  # 拿取分类小类
        except:
            small_type = ' '
            CLICK_REGION(driver, soup, name, filename, small_type)
            continue

        get_more=driver.find_element_by_xpath('//*[@id="classfy-sub"]/a[last()]').text #拿取列表最后一个值是否为更多
        if get_more=='更多':
            driver.find_element_by_xpath('//*[@id="classfy-sub"]/a[last()]').click() #点击更多按钮
            time.sleep(1)
            soup = GET_SOUP(driver)
            type_small_list = soup.find('div', attrs={'id': "classfy-sub"}).find_all('a')
            small_step=len(type_small_list)
        else:
            small_step = len(type_small_list) + 1

        start = MARKING('small_type', '', 2)

        for h in range(start,small_step):
            time.sleep(5)

            try:
                driver.find_element_by_xpath('//div[@class="nav-category nav-tabs J_filter_region"]/a[1]/span').click()  # 每次区域循环完成需要把区域重新点击回去
                time.sleep(2)
            except:
                driver.refresh()
                time.sleep(2)
                driver.find_element_by_xpath('//div[@class="nav-category nav-tabs J_filter_region"]/a[1]/span').click()  # 每次区域循环完成需要把区域重新点击回去
                time.sleep(2)

            if  h==15 and get_more=='更多':
                try:
                  driver.find_element_by_xpath('//*[@id="classfy-sub"]/a[last()]').click()#点击更多按钮
                  soup=GET_SOUP(driver)
                except:
                   pass

            small_type=type_small_list[h-1].find('span').next
            button = '//*[@id="classfy-sub"]/*/span[text()="'+small_type+'"]'

            try:
                driver.find_element_by_xpath(button).click()  # 点击分类小类
                time.sleep(3)
                print('###############################################分类小类：%s' % small_type)
            except:
                driver.find_element_by_xpath('//*[@id="classfy-sub"]/a[1]/span').click()  # 页面排版出现变动，点击不限
                time.sleep(3)
                if h == 15 and get_more=='更多':
                    try:
                        driver.find_element_by_xpath('//*[@id="classfy-sub"]/a[last()]').click()  # 点击更多按钮
                    except:
                        pass
                driver.find_element_by_xpath(button).click()# 点击分类小类
                time.sleep(3)
                print('###############################################分类小类：%s' % small_type)

            GetLog('dzdp', '###############################################分类小类：%s' %small_type)


            MARKING('small_type', h, 1)

            CLICK_REGION(driver, soup,name,filename,small_type)

            small_type_temp = MARKING('small_type', '', 2)  # 当小类型循环执行完的时候把开始步数重新设置为2
            if small_type_temp == small_step-1:
                print('开始小类型重新设置为2')
                MARKING('small_type', 2, 1)



def CLICK_NEXT(driver,soup,name,filename,small_type,big_region,small_region):
    global if_start
    try:
        max_page = soup.find('div', class_='page').find_all('a')[-2].next
        print('分页数:%d'%int(max_page))
    except Exception as e:
        print('是否没有分页，请查看')
        GetLog('dzdp', '是否没有分页，请查看')
        print(e)
        return -1


    start=MARKING('page', '', 2)
    if if_start == 0 and start!=1:
        print('继续上次的分页号数执行')
        time.sleep(3)
        current_url=driver.current_url
        now_url='%sp%s' %(current_url,str(int(start)-1))
        driver.get(now_url)
        print('继续上次的分页号数执行')
        time.sleep(3)

    if_start = 1
    while start < int(max_page):
        try:
            #driver.find_element_by_xpath('//*[@id="top"]/div[6]/div[3]/div[1]/div[2]/a[last()]').click()   #点击下一页
            #driver.find_element_by_link_text("下一页").click()    #点击下一页
            driver.find_element_by_xpath('//div[@class="page"]/a[last()]').click()   #点击下一页
            time.sleep(3)
            MARKING('page', start, 1)
            soup=GET_SOUP(driver)
        except Exception as e:
            driver.refresh()
            time.sleep(3)
            print('点击下一页有问题')
            print(e)
            continue
        try:
          print('执行下一步里的函数')
          SHOP_BASIS_INFO(name, soup, filename,small_type,big_region,small_region)
          print('下一步里的函数执行成功')
        except Exception as e:
            print('函数错误')
            traceback.print_exc()
            GetLog('dzdp', '[ERROR:][ERROR:][ERROR:]%s_%s_%s错误' % (small_type,big_region,small_region))
            driver.find_element_by_xpath('//div[@class="page"]/a[1]').click()  # 点击上一页
            time.sleep(3)
            continue
        print('###第%d页' % (start + 1))
        GetLog('dzdp', '####第%d页' % (start + 1))
        time.sleep(1)
        start = start + 1

    print('循环完毕后吧页数重置为1')
    MARKING('page', 1, 1)  #循环完毕后吧页数重置为1

    return  1


# 商铺基础信息处理
def SHOP_BASIS_INFO(name, soup, filename,small_type,big_region,small_region):
    if name == 'meituan':
        channel_type = 1
    elif name == 'dzdp':
        channel_type = 2

    type = 3
    dzdp_list = []
    shop_list = []
    # file='C:/Users/Administrator/Desktop/%s_%s.txt' %(name,filename)
    detail_address = 'detail_address'
    #soup = BeautifulSoup(data, "html.parser")
    body_data = soup.find('div', attrs={'class': 'shop-list J_shop-list shop-all-list'})
    res_list = body_data.find_all('li')
    for res in res_list:

        shop_web_address = res.find('a', attrs={'target': '_blank'}).get('href')  # 商店网址

        shop_id = shop_web_address.split('/')[-1]  # 商铺ID

        img_address = res.find('img').get('src')  # 图片地址

        shop_name = res.find('h4').next  # 商铺名称

        star_level = res.find('span', attrs={'class': 'sml-rank-stars'}).get('class')[1]  # 商铺星级

        try:
            mean_price = res.find('a', attrs={'class': 'mean-price'}).find('b').next  # 人均
        except:
            mean_price = '-'  # 人均

        shop_type = res.find('div', attrs={'class': 'tag-addr'}).find_all('span')[0].next  # 商铺类型

        shop_address = '%s %s' % (res.find('div', attrs={'class': 'tag-addr'}).find_all('span')[1].next,
                                  res.find('div', attrs={'class': 'tag-addr'}).find_all('span')[2].next)  # 商铺地址

        try:
            shop_socre = '质量：%s 环境：%s 服务：%s ' % (
            res.find('span', attrs={'class': 'comment-list'}).find_all('span')[0].find('b').next, res.find('span', attrs={ 'class': 'comment-list'}).find_all('span')[1].find('b').next,res.find('span', attrs={'class': 'comment-list'}).find_all('span')[2].find('b').next)  # 店铺评分
        except:
            shop_socre = ' '

        shop_info = '%s[}%s[}%s[}%s[}%s[}%s[}人均：%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s[}%s' % (
        shop_id, shop_name, shop_web_address, img_address, star_level, ' ', mean_price, shop_type, shop_socre,
        shop_address, channel_type, ' ',small_type,big_region,small_region)
        get_detail_address = '%s[}%s' % (shop_web_address, shop_type)

        GetFile(basicfilename, shop_info, type,5000)
        GetFile(webaddressfilename, get_detail_address, type,5000)

        dzdp_list.append(shop_info)
        shop_list.append(shop_web_address)

    return shop_list


##拿出列表数据
def GET_BASIC(name, filename, url):
    chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe")
    os.environ["webdriver.chrome.driver"] = chrome_driver
    driver = webdriver.Chrome(chrome_driver)
    driver.set_page_load_timeout(100)
    driver.set_script_timeout(100)
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_xpath('//*[@id="classfy"]/a[last()]').click()#点击更多
    soup = GET_SOUP(driver)
    CLICK_TYPE(driver, soup, name, filename)
    #SHOP_BASIS_INFO(name, soup, filename, '', '', '')
    driver.quit()





