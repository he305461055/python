from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import urllib
import html.parser
import time
import re
import POI
import os
from scrapy.selector import Selector

#log_dir='C:/Users/Administrator/Desktop/DZDP_BASIC/detail/'
img_dir='D:/photo/20171019/'
config_dir='E:/python/DZDP_SPIDERS/config/'
data_dir='C:/Users/Administrator/Desktop/'

#写入日志
'''
def GET_LOG(name,data):
    datetime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    date=time.strftime("%Y-%m-%d",time.localtime())
    data='[%s]%s:::::%s' %(str(datetime),str(date),data)
    file = '%s%s_%s_%s.txt' % (log_dir,name, 'LOG',str(date))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')
'''
#下载图片
def GetImg(url,img_name):
    urllib.request.urlretrieve(url, '%s%s' % ('D:/photo/yyzz/', img_name))

def MARKING(filename,value,type):
    file='%s%s.txt' %(config_dir,filename)
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
def GET_FILE(name,filename,data,type,count):
    # 没有文件的话生成文件
    if os.path.exists(r'%s%s_variable.txt' %(config_dir,filename)):
        pass
    else:
        with open('%s%s_variable.txt' %(config_dir,filename), 'w', encoding='utf-8') as f:
            pass

    variable = len(open('%s%s_variable.txt' %(config_dir,filename),encoding='utf-8').readlines())
    file='%s%s_%s_%d.txt' % (data_dir,name, filename,variable)
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
            file = '%s%s_%s_%d.txt' % (data_dir,name, filename, variable)
            with open(file, 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')

#拿取详单数据
def GET_DETAIL_HTML(driver,url):

    time.sleep(1)
    driver.get(url)
    try:
      driver.find_element_by_xpath('//*[@id="basic-info"]/a').click()
    except:
        pass
    htmldata=driver.page_source
    #整体数据
    #html_parser = html.parser.HTMLParser()
    #data = html_parser.unescape(data)
    #点击数据
    data=Selector(text=htmldata)

    img_regex = r'(.*?(?:.jpg|.png|.jpeg|.bmp|.svg|.swf)+)'  # 图片正则
    shop_id = url.split('/')[-1]  # 店铺ID

    try:
        try:
          shop_name = data.xpath('//*[@id="basic-info"]/h1/text()').extract()[0].replace('\n','')  # 店铺名称
        except:
          shop_name = data.xpath('//h1[@class="shop-title"]/text()').extract()[0].replace('\n', '')  # 店铺名称
    except:
        try:
          shop_name = data.xpath('//div[@class="hotel-title clearfix"]/h1/text()').extract()[0].replace('\n', '')  # 店铺名称
        except:
          shop_name = data.xpath('//div[@class="shop-name"]/h1/text()').extract()[0].replace('\n', '')  # 店铺名称
    try:
        original_shop_img_adress = data.xpath('//img[@itemprop="photo"]/@src').extract()[0]  # 原始商铺图片地址
        shop_img_adress = re.findall(img_regex, original_shop_img_adress)[0].split('/')[-1]  # 商铺图片
    except:
        shop_img_adress = ' '

    pattern = re.compile('poi: "(.*?)"', re.S)  # 获取坐标
    try:
        poi = re.findall(pattern, str(data.extract()))[0]
        coordinate = str(POI.decode(poi))
    except:
        coordinate = ' '

    try:
        shop_sorce_list = data.xpath('//div[@class="brief-info"]/span')
        shop_stars = shop_sorce_list[0].xpath('@class').extract()[0].split(' ')[-1]  # get('class')[1]  # 商铺星级
    except:
        shop_stars=' '


    mean_price = ''


    shop_sorce = ' '

    try:
        try:
            shop_address = data.xpath('//span[@itemprop="street-address"]/text()').extract()[0].replace('\n', '').replace(' ', '')# 商铺地址
        except:
            try:
              shop_address = data.xpath('//div[@class="address"]/text()').extract()[0].replace('\n','').replace(' ','').replace('"','') # 商铺地址
            except:
              shop_address = data.xpath('//p[@class="shop-contact address"]/span/@title').extract()[0].replace('\n', '').replace(' ', '')  # 商铺地址
    except:

        try:
            shop_address = data.xpath('//span[@itemprop="street-address"]/text()').extract()[0].replace('\n', '').replace(
                ' ', '') # 商铺地址
        except:
            shop_address = data.xpath('//span[@class="hotel-address"]/text()').extract()[0].replace('\n',
                                                                                                        '').replace(
                ' ', '')  # 商铺地址

    try:
        try:
            shop_phone = ' '.join(data.xpath('//p[@class="expand-info tel"]/span/text()').extract())  # 商铺电话
        except:
            shop_phone = ' '.join(data.xpath('//ul[@class="list-info"]/li[1]/div[2]/text()').extract())  # 商铺电话
    except:
        try:
           shop_phone = ' '.join(data.xpath('//div[@class="shop-contact telAndQQ"]/span/strong/text()').extract())  # 商铺电话
        except:
           shop_phone = ' '

    shop_phone1 = ''

    shop_charge = ''

    try:
        shop_time = ' '.join(data.xpath('//p[@class="info info-indent"]/span/text()').extract()).replace('\n','').replace( ' ', '')  # 商铺营业时间
    except:
        shop_time = ' '

    shop_service = ''

    shop_info = ''


    channel_type = 2

    create_time = ''

    pay_play = ''

    shop_park = ''

    comment_list = data.xpath('//div[@class="content"]/span/a/text()').extract()  # 点评
    if len(comment_list) > 0:
        comment = ','.join(comment_list)
    else:
        comment = ' '

    shop_type = '>'.join(data.xpath('//*[@id="body"]/div[2]/div[1]/a/text()').extract()).replace('\n', '').replace(
        ' ', '')  # 店铺类型

    # regex = re.compile("licensePics:(.*?),]",re.S)
    # regex = r"licensePics:\[\\'(.*?)\\',\]"

    regex = r"licensePics:\[\\'(.*?)\\',\]"

    business_list = re.findall(regex, str(data.extract()))
    if len(business_list) > 0:
        business_list = business_list[0].split(',')

    if len(business_list) > 0:
        original_business_licence = business_list[0].replace('\\', '').replace("'", '')
        temp_business_licence = re.findall(img_regex, original_business_licence.split('/')[-1].split('?')[0])
        if len(temp_business_licence) == 0:
            business_licence = '%s.jpg' % (original_business_licence.split('/')[-1].split('?')[0])
        else:
            business_licence = temp_business_licence[0]

    else:
        original_business_licence = ' '
        business_licence = ' '

    if len(business_list) > 1:
        original_beverage_license = business_list[1].replace('\\', '').replace("'", '')
        temp_beverage_license = re.findall(img_regex, original_beverage_license.split('/')[-1].split('?')[0])
        if len(temp_beverage_license) == 0:
            beverage_license = '%s.jpg' % (original_beverage_license.split('/')[-1].split('?')[0])
        else:
            beverage_license = temp_beverage_license[0]
    else:
        original_beverage_license = ' '
        beverage_license = ' '

    shop_detail_info = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s[}%s[}%s' % (
        shop_id, shop_name, shop_img_adress, coordinate, shop_stars, shop_sorce, shop_address,
        shop_phone, shop_phone1, shop_charge, mean_price, shop_time, shop_service, shop_info, channel_type, create_time,
        pay_play, shop_park, comment, shop_type)

    shop_attached = '%s[}%s[}%s[}%s[}%s[}%s[}%s' % (
    shop_id, business_licence, original_business_licence, beverage_license, original_beverage_license, ' ', ' ')

    for sel in data.xpath('//ul[@class="comment-list J-list"]/li'):
        try:
            user_name = sel.xpath('p/a[@class="name"]/text()').extract()[0]  # 用户名称

            content_sorce = sel.xpath('div/p[@class="shop-info"]/span')
            content_stars = content_sorce[0].xpath('@class').extract()[0].split()[-1]  # 评分星级
            content_sorce = ' '.join(content_sorce.xpath('text()').extract())  # 用户评分

            user_content = ''.join(sel.xpath('*//p[@class="desc J-desc"]/text()').extract())
            if len(user_content) < 1:
                user_content = ''.join(sel.xpath('*//p[@class="desc"]/text()').extract())

            content = '%s[}%s[}%s[}%s[}%s[}%d{]' % (
            shop_id, user_name, content_stars, content_sorce, user_content, channel_type)
        except:
            continue
        with open('C:/Users/Administrator/Desktop/shop_content.txt', 'a', encoding='utf-8') as f:
            f.write(content)
            f.write('\n')
        '''
        content_item = ContentItem()
        content_item['shop_id'] = shop_id
        content_item['user_name'] = user_name
        content_item['content_stars'] = content_stars
        content_item['content_sorce'] = content_sorce
        content_item['user_content'] = user_content
        content_item['channel_type'] = channel_type
        yield content_item
      '''
    with open('C:/Users/Administrator/Desktop/shop_detail.txt', 'a', encoding='utf-8') as f:
        f.write(shop_detail_info)
        f.write('\n')
    # '''
    # 下载图片
    try:
        if shop_img_adress != ' ' and 'http:' in original_shop_img_adress:
            GetImg(original_shop_img_adress, shop_img_adress)
    except Exception as e:
        print(e)
        print(original_shop_img_adress)
        with open('C:/Users/Administrator/Desktop/error_img', 'a', encoding='utf-8') as f:
            f.write(original_shop_img_adress)
            f.write('\n')
        print('无法下载请检查路径')
        return None

    try:
        if business_licence != ' ' and 'http:' in original_business_licence:
            GetImg(original_business_licence, business_licence.split('/')[-1].split('?')[0])
    except Exception as e:
        print(e)
        print(original_business_licence)
        with open('C:/Users/Administrator/Desktop/error_img', 'a', encoding='utf-8') as f:
            f.write(original_business_licence)
            f.write('\n')
        print('无法下载请检查路径')
        return None

    try:
        if beverage_license != ' ' and 'http:' in original_beverage_license:
            GetImg(original_beverage_license, beverage_license.split('/')[-1].split('?')[0])
    except Exception as e:
        print(e)
        print(original_beverage_license)
        with open('C:/Users/Administrator/Desktop/error_img', 'a', encoding='utf-8') as f:
            f.write(original_beverage_license)
            f.write('\n')
        print('无法下载请检查路径')
        return None

    # 写入商铺资质
    if (beverage_license != ' ' or business_licence != ' '):
        with open('C:/Users/Administrator/Desktop/shop_shop_attached.txt', 'a', encoding='utf-8') as f:
            f.write(shop_attached)
            f.write('\n')
    # '''


'''
#商铺详细信息
def SHOP_DETAILS_INFO_1(name,filename,url):
    if name=='meituan':
        channel_type=1
    elif name=='dzdp':
        channel_type=2

    type=3

    file='C:/Users/Administrator/Desktop/%s.txt' %filename
    (data, business_licence, beverage_license)=GET_DETAIL_HTML(name,url)
    soup=BeautifulSoup(data,'html.parser')
    response=Selector(text=data).xpath("//td[@class='zwmc']/div/a")
    regex = r"licensePics:\[\\'(.*?)\\',\]"
    img_regex = r'(.*?(?:.jpg|.png|.jpeg|.bmp|.svg|.swf)+)'  # 图片正则
    business_list = re.findall(regex, str(soup))
    if len(business_list) > 0:
        business_list = business_list[0].split(',')

    if len(business_list) > 0:
        original_business_licence = business_list[0].replace('\\', '').replace("'", '')
        temp_business_licence = re.findall(img_regex, original_business_licence.split('/')[-1].split('?')[0])
        if len(temp_business_licence) == 0:
            business_licence = '%s.jpg' % (original_business_licence.split('/')[-1].split('?')[0])
        else:
            business_licence = temp_business_licence[0]

    else:
        original_business_licence = ' '
        business_licence = ' '

    if len(business_list) > 1:
        original_beverage_license = business_list[1].replace('\\', '').replace("'", '')
        temp_beverage_license = re.findall(img_regex, original_beverage_license.split('/')[-1].split('?')[0])
        if len(temp_beverage_license) == 0:
            beverage_license = '%s.jpg' % (original_beverage_license.split('/')[-1].split('?')[0])
        else:
            beverage_license = temp_beverage_license[0]
    else:
        original_beverage_license = ' '
        beverage_license = ' '

    body_data=soup.find('div',attrs={'class':'body'})

    pattern = re.compile('poi: "(.*?)"', re.S)  # 获取坐标
    try:
        poi = re.findall(pattern, str(data))[0]
        coordinate = str(POI.decode(poi))
    except:
        coordinate = ' '

    shop_id = url.split('/')[-1]  # 店铺ID

    shop_type = '>'.join(response.xpath('//*[@id="body"]/div[2]/div[1]/a/text()').extract()).replace('\n', '').replace( ' ', '')  # 店铺类型

    try:
        shop_name = body_data.find('h1', class_="shop-name").next.strip().replace('"', '').replace('\n', '')#店铺名称
    except:
      shop_name =  body_data.find('div', class_="shop-name").find('h2').next.strip().replace('"','').replace('\n','') #店铺名称

    try:
        original_shop_img_adress=body_data.find('img',itemprop="photo").get('src') #商铺图片
        shop_img_adress = re.findall(img_regex, original_shop_img_adress)[0].split('/')[-1]  # 商铺图片
    except:
        shop_img_adress=' '

    shop_sorce_list=body_data.find('div',attrs={'class':'brief-info'}).find_all('span')
    shop_stars = shop_sorce_list[0].get('class')[1]  # 商铺星级

    mean_price = shop_sorce_list[2].next  # 人均
    if '人均' not in mean_price:
        mean_price = shop_sorce_list[1].next  # 人均

    if len(shop_sorce_list)>3:
       shop_sorce = '%s %s %s' % (shop_sorce_list[-3].next, shop_sorce_list[-2].next, shop_sorce_list[-1].next)  # 商铺评分
    else:
       shop_sorce=' '


    shop_address=body_data.find('span',attrs={'itemprop':'street-address'}).next.strip() #商铺地址

    try:
        temp_list = []
        shop_phone_list=body_data.find('p',attrs={'class':'expand-info tel'}).find_all('span') #商铺电话
        for i in shop_phone_list:
            temp_list.append(i.next)
        shop_phone=' '.join(temp_list)
    except:
        shop_phone=' '

    try:
       shop_time=body_data.find('p',attrs={'class':'info info-indent'}).find_all('span')[1].next.strip() #商铺营业时间
    except:
       shop_time=' '

    try:
        commnet = []
        comment_list = body_data.find('div', attrs={'class': 'content'}).find_all('span')  #点评
        for i in comment_list:
            commnet.append(i.text)
        comment = ','.join(commnet)
    except:
        comment=' '

    shop_phone1=' '
    shop_charge = ''
    shop_service = ''
    shop_info = ''
    create_time = ''
    pay_play = ''
    shop_park = ''

    shop_detail_info = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s[}%s[}%s' % ( shop_id, shop_name, shop_img_adress, coordinate, shop_stars, shop_sorce, shop_address,
        shop_phone, shop_phone1, shop_charge, mean_price, shop_time, shop_service, shop_info, channel_type, create_time, pay_play, shop_park, comment, shop_type)
    shop_attached = '%s[}%s[}%s[}%s[}%s[}%s[}%s' % (shop_id, business_licence, original_business_licence, beverage_license, original_beverage_license, ' ', ' ')
    try:
      USER_CONTENT_1(name,shop_id,body_data)
    except:
     pass

    GET_FILE(name,filename,shop_detail_info,type,5000)


    # 下载图片
    try:
        if shop_img_adress != ' ' and 'http:' in original_shop_img_adress:
            tool.GetImg(original_shop_img_adress, shop_img_adress)
    except Exception as e:
        print(e)
        print(original_shop_img_adress)
        print('无法下载请检查路径')
        return None

    try:
        if business_licence != ' ' and 'http:' in original_business_licence:
            tool.GetImg(original_business_licence, business_licence.split('/')[-1].split('?')[0])
    except Exception as e:
        print(e)
        print(original_business_licence)
        print('无法下载请检查路径')
        return None

    try:
        if beverage_license != ' ' and 'http:' in original_beverage_license:
            tool.GetImg(original_beverage_license, beverage_license.split('/')[-1].split('?')[0])
    except Exception as e:
        print(e)
        print(original_beverage_license)
        print('无法下载请检查路径')
        return None

    #写入商铺资质
    if (beverage_license!=' 'or business_licence!=' '):
        GET_FILE(name, 'intelligence', shop_attached, type,5000)

def SHOP_DETAILS_INFO_2(name,filename,url):
    if name=='meituan':
        channel_type=1
    elif name=='dzdp':
        channel_type=2

    type=3
    temp_list = []
    file = 'C:/Users/Administrator/Desktop/%s.txt' % filename
    (data, business_licence, beverage_license) = GET_DETAIL_HTML(name, url)
    # with open('C:/Users/Administrator/Desktop/foo4.txt', 'r') as f:
    #  data=f.read()
    soup = BeautifulSoup(data, 'html.parser')

    body_data = soup.find('div', attrs={'class': 'page-main'})

    pattern = re.compile('poi: "(.*?)"', re.S)  # 获取坐标
    poi = re.findall(pattern, data)[0]
    coordinate = POI.decode(poi)
    print(coordinate)

    shop_id = url.split('/')[-1]  # 店铺ID

    shop_address = body_data.find('a', attrs={'class': 'link-dk'}).next.strip()  # 商场地址

    pattern = re.compile('<span class="title">营业时间：</span>(.*?)</p>')  # 商场营业时间
    shop_time = re.findall(pattern, data)[0]  # 商场营业时间

    pattern1 = re.compile('<span class="title">联系电话：</span>(.*?)</p>', re.S)  # 商场电话
    shop_phone = re.findall(pattern1, data)[0].strip()  # 商场电话

    try:
        pattern2 = re.compile('<span class="title">停车信息：</span>(.*?)<a', re.S)  # 停车信息
        shop_park = re.findall(pattern2, data)[0].strip()  # 停车信息
    except:
        shop_park = ' '

    try:
        pattern3 = re.compile('<span class="title">人均消费：</span>(.*?)</p>', re.S)  # 人均消费
        mean_price = re.findall(pattern3, data)[0].strip()  # 人均消费
    except:
        mean_price = ' '

    try:
     USER_CONTENT_1(name,shop_id,body_data)
    except:
      pass

    shop_detail_info = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s'  % (shop_id,' ',' ', coordinate,' ',' ', shop_address, shop_phone,' ', mean_price, shop_time,' ', ' ',channel_type,' ',' ',shop_park,' ')

    GET_FILE(name, filename, shop_detail_info,type,2000)


def SHOP_DETAILS_INFO_3(name, filename, url):
    if name=='meituan':
        channel_type=1
    elif name=='dzdp':
        channel_type=2
    type=3
    temp_list = []
    (data, business_licence, beverage_license) = GET_DETAIL_HTML(name, url)
    # with open('C:/Users/Administrator/Desktop/foo4.txt', 'r') as f:
    #  data=f.read()
    soup = BeautifulSoup(data, 'html.parser')
    body_data = soup.find('div', attrs={'id': 'main-body'})

    pattern=re.compile('poi: "(.*?)"',re.S)  #获取坐标
    poi=re.findall(pattern,data)[0]
    coordinate=POI.decode(poi)
    print(coordinate)

    shop_id=url.split('/')[-1] #店铺ID

    shop_name=body_data.find('h1',attrs={'class':'shop-title'}).next #店铺名称

    shop_sorce_list = body_data.find('div', attrs={'class': 'comment-rst'}).find_all('span')
    shop_stars = shop_sorce_list[0].get('class')[1]  # 商铺星级
    mean_price = shop_sorce_list[1].next  # 人均
    shop_sorce = ' '  # 商铺评分


    try:
        shop_address = body_data.find('span', attrs={'class': 'f1 road-addr'}).next.strip()  # 商铺地址
    except:
        shop_address = body_data.find('div', attrs={'class': 'shop-addr'}).find('span').get('title')  # 商铺地址

    try:
        shop_phone = body_data.find('span', attrs={'class': 'icon-phone'}).next  # 商铺电话
    except:
        shop_phone = body_data.find('div', attrs={'class': 'shopinfor'}).find_all('span')[0].next  # 商铺电话

    try:
        shop_time = body_data.find_all('div', attrs={'class': 'js-more-item more-item Hide'})[1].find( 'span').next  # 商铺营业时间
    except:
        shop_time = body_data.find('div', attrs={'class': 'more-class '}).find_all('p')[1].find('span').next  # 商铺营业时间

    try:
       USER_CONTENT_2(shop_id,body_data)
    except:
        pass

    shop_detail_info = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s'  % (shop_id, ' ',' ', coordinate,' ',' ', shop_address, shop_phone,' ', mean_price, shop_time,' ', ' ',channel_type,' ',' ',' ',' ')

    GET_FILE(name, filename, shop_detail_info,type,2000)


# 评论1
def USER_CONTENT_1(name,id,body_data):
    if name=='meituan':
        channel_type=1
    elif name=='dzdp':
        channel_type=2
    type=3
    filename = 'food_user_content'
    content_data = body_data.find('ul', attrs={'class': 'comment-list J-list'})
    content_list = content_data.find_all('li')
    for i in content_list:
        user_name = i.find('a', attrs={'class': 'name'}).next  # 用户名称

        content_sorce = i.find('p', attrs={'class': 'shop-info'}).find_all('span')
        content_stars = content_sorce[0].get('class')[1]  # 评分星级
        content_sorce = '%s %s %s' % (content_sorce[1].next, content_sorce[2].next, content_sorce[3].next)  # 用户评分

        try:
            user_content = i.find('p', attrs={'class': 'desc J-desc'}).getText('\n').strip()  # 用户评论
        except:
            user_content = i.find('p', attrs={'class': 'desc'}).getText('\n').strip()   # 用户评论

        content='%s[}%s[}%s[}%s[}%s[}%d{]' %(id,user_name,content_stars,content_sorce,user_content,channel_type)

        GET_FILE(name, filename, content,type,5000)

# 用户评论2
def USER_CONTENT_2(name,id,body_data):
    if name=='meituan':
        channel_type=1
    elif name=='dzdp':
        channel_type=2
    type=3
    filename = 'dzdp_user_content'
    file = 'C:/Users/Administrator/Desktop/%s.txt' % filename
    content_data = body_data.find('div', attrs={'class': 'comment-list'})
    content_list = content_data.find_all('div',attrs={'class':'content'})
    for i in content_list:
        user_name = i.find('p', attrs={'class': 'name'}).next  # 用户名称

        content_sorce = i.find('div', attrs={'class': 'user-info'}).find_all('span')
        content_stars = content_sorce[0].get('class')[1]  # 评分星级

        try:
            user_content = i.find('div', re.compile("desc J_brief-cont-long Hide")).getText('\n').strip()# 用户评论
            print('****************************')
        except:
            try:
                user_content = i.find('div',re.compile("desc J_brief-cont")).getText('\n').strip()  # 用户评论
                print('#############################')
            except:
                user_content = i.find('div', re.compile("J_brief-cont")).getText('\n').strip()  # 用户评论

        content = '%s[}%s[}%s[}%s[}%s[}%d' % (id, user_name, content_stars, content_sorce, user_content,channel_type)

        GET_FILE(name, filename, content,type,5000)
'''


