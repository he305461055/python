import pymysql
import time
import re
#import address

config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'spiders',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

# 返回可用于multiple rows的sql拼装值
def multipleRows(params):
    ret = []
    # 根据不同值类型分别进行sql语法拼装
    for param in params:
        if isinstance(param, (int,  float, bool)):
            ret.append(str(param))
        elif isinstance(param, (str, 'utf-8')):
            param=param.replace('"','\\"')
            ret.append( '"' + param + '"' )
        else:
            print('unsupport value: %s ' % param)
    return '(' + ','.join(ret) + ')'

def insert_query(sql, datas):
    connection = pymysql.connect(**config)
    count=0
    with  connection.cursor() as cursor:
        for data in datas:
            value=[]
            s=0
            for item in data.split('[}'):
            #for item in data.split(','):
                 #if s==3:
                value.append(item.replace('\n','').replace('﻿','').replace(' ',''))
                 #s=s+1
            query_sql = "%s %s;" % (sql,multipleRows(value))
            # else:
            #  query_sql = "%s and %s" % (sql, condition)
            #print(query_sql)
            try:
              cursor.execute(query_sql)
              count=count+1
            except pymysql.err.IntegrityError as e:
              pass
              #print('主键重复')
              #print(sql)
              #time.sleep(10)
            except Exception as e:
                  print(e)
                  print(query_sql)
                  print('特殊处理')
                  with open('C:/Users/Administrator/Desktop/大众插入出错数据.txt','a',encoding='utf-8') as f:
                      f.write(sql)
                      f.write('\n')
        connection.commit()
    connection.close()
    print('本次共插入%d条' %count)


#sql='insert into shop_basic(shop_id,shop_name,shop_web_address,shop_img_address,shop_socre_star_level,min_price,mean_price,shop_type,shop_socre,shop_address,channel_type,rated_num,small_type,big_region,small_region) VALUES '
#sql='insert into shop_detail(shop_id,shop_name,shop_img_address,shop_poi,shop_stars,shop_sorce,shop_address,shop_phone,shop_charge,mean_price,shop_time,shop_service,shop_info,channel_type,create_time,pay_play,shop_park,comment) VALUES '
sql='insert into shop_detail(shop_id,shop_name,shop_img_address,shop_poi,shop_stars,shop_sorce,shop_address,shop_phone,shop_phone1,shop_charge,mean_price,shop_time,shop_service,shop_info,channel_type,create_time,pay_play,shop_park,comment,shop_type) VALUES '
#sql='insert into user_content(shop_id,user_name,content_stars,content_sorce,user_content,channel_type) VALUES '
#sql='insert into city_gdp(city,level,province,gdp) VALUES '
#sql='insert into city_shop_num(city,shop_num,mark) VALUES '
#sql='insert into dai1(id,name,type,create_time,mark,people,price,hangye_classify,pingtai_classify,success,info,text)VALUES '
#sql='insert into dai2(id, web_address,address,phone,email) VALUES '
#sql='insert into meituanshop(url,shopname,star,shopsold,shopright,shoptime,startprice,deliveryfee,CBD) values'
#sql='insert into shopdetail(url,shopname,phone1,phone2,phone3,address,time,delivery) values'
#sql='insert into test2(shopname,url,address) values'
#sql='insert into test1(shopname,address,phone) values'
#sql='insert into meituanshop2017(id,fristurl, textname, shopname, address, phone,img, time,businessLicenceImg, type) value'
#sql='insert into pipei_2017(id1,name,address,peple,id2,id3) value'
#sql='insert into shop_detail_2017(shop_id,shop_name,shop_img_address,shop_poi,shop_stars,shop_sorce,shop_address,shop_phone,shop_phone1,shop_charge,mean_price,shop_time,shop_service,shop_info,channel_type,create_time,pay_play,shop_park,comment,shop_type) VALUES '
#sql='insert into shop_hj(shop_id, img) values'
#sql='insert into ywy(id,cat, shop_name,address,faren,dt,peple,yy) values'
#sql='insert into type(type, s_type) values'
#sql='insert into newimg(id,shop_id,name,firstimg,bizimg,logo,newbizimg,hjimg) VALUES '
#sql='insert into meishi(id1,name,address,shopname,type) VALUES '
#sql='insert into meituanshop(id,shopname,address,street,street_number,phone,time1,time2,bizimg,type,iszz) VALUES '
#sql='insert into meituanbasic(id,shopname,address,avgprice,logo,logname,lowestprice,lat,lng,avgscore,comments,backCateName,district,street) VALUES '
#sql='insert into street_code(region,region_code,street_code,street_name) VALUES'

def get_sql(sql,file_name):
    datas=[]
    path='C:/Users/Administrator/Desktop/DZDP_BASIC/food/'
    for i in range(14,18):
        with open('%s%s_%d.txt' %(path,file_name,i),'r',encoding='utf-8') as f:
            for line in f:
                datas.append(line.replace('\n','').replace(' ',''))

    '''
    #专门给用户评论表用的
    path='C:/Users/Administrator/Desktop/DZDP_BASIC/'
    filename='dzdp_food_user_content'
    datas=[]
    for i in range(70,85):
        with open('%s%s_%d.txt' %(path,filename,i),'r',encoding='utf-8') as f:
            x = re.findall('\d{5,10}\[\}.*?\{\]', f.read().replace('\n',''))
            for line in x:
                datas.append(line.replace('\n',''))
    datas1=[]
    for j in datas:
        r=re.findall(u"[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']",j.split('[}')[4])
        str1 = ''.join(r)
        str2='%s[}%s[}%s[}%s[}%s[}%s' %(j.split('[}')[0],j.split('[}')[1],j.split('[}')[2],j.split('[}')[3],str1,j.split('[}')[5].replace('{]',''))
        datas1.append(str2)
    datas=[]
    datas=datas1

    #aa=['17713272','totoiloveyou','sml-str40','口味：3 环境：2 服务：2','总体4星，干碟味道好，冒脑花也好吃，里面豆芽可以，冷锅串串，小郡肝牛肉都不错，就是服务员大妈听力太差，喊半天喊不答应，一瓶纯生都能听成一瓶豆奶，我去，太可以了。味道还是巴适，还会再去。两个人吃了161，还是不便宜啊，大众点评95折，省了8块多。','2']
    #multipleRows(aa)

    '''
    print('本次共有%d条' %(len(datas)))
    insert_query(sql,datas)
    #'''
    '''
    connection = pymysql.connect(**config)
    with  connection.cursor() as cursor:
        cursor.execute("CREATE  TABLE aa AS SELECT b.city,c.province, b.shop_num,c.gdp FROM city_shop_num b LEFT JOIN city_gdp c ON b.city=c.city")
        resutl=cursor.fetchall()
        print(resutl)
    connection.close()
    '''
get_sql(sql,'dzdp_food_detail')
'''
success=[]
#with open('C:/Users/Administrator/Desktop/20171031.txt', 'r', encoding='utf-8') as f:
#    for line in f:
#        success.append(line.split('[}')[0].replace('\n', '').replace(' ', '').replace('\ufeff',''))
#print(type)
import xlrd
wb = xlrd.open_workbook('C:/Users/Administrator/Desktop/匹配20171031.xlsx')  # 打开文件
sh = wb.sheet_by_name('Sheet4')

sh = wb.sheet_by_index(0)  # 第一个表

sheetNames = wb.sheet_names()  # 查看包含的工作表

# 获得工作表的两种方法
sh = wb.sheet_by_index(0)
sh = wb.sheet_by_name(u'Sheet4')

# 单元格的值
cellA1 = sh.cell(0, 0)
cellA1Value = cellA1.value

# 第一列的值
columnValueList1 = sh.col_values(0)
columnValueList2 = sh.col_values(1)
#columnValueList3 = sh.col_values(2)
#columnValueList4 = sh.col_values(3)
#columnValueList5 = sh.col_values(4)
#columnValueList6 = sh.col_values(5)
#columnValueList7 = sh.col_values(6)
#columnValueList8 = sh.col_values(7)
#columnValueList9 = sh.col_values(8)
#columnValueList10 = sh.col_values(9)
#columnValueList11 = sh.col_values(10)
#columnValueList12 = sh.col_values(11)
#columnValueList13 = sh.col_values(12)
#columnValueList14 = sh.col_values(13)
#columnValueList15 = sh.col_values(14)


unionlist=list(zip(columnValueList1,columnValueList2)) #,columnValueList3,columnValueList4,columnValueList5,columnValueList6,
                   #columnValueList7,columnValueList8,columnValueList9,columnValueList10,columnValueList11,columnValueList12,
                   #columnValueList13,columnValueList14,columnValueList15
                   #))

for line in unionlist:
    print(line)
    line=list(line)
    line[0] = str(line[0]).replace('\n','').replace(' ', '')
    #if line[0] in success:
    #    continue
    #if line[1]=='':
    #    continue
    line[1] = str(line[1]).replace('\n','').replace(' ', '')
    #line[2] = str(line[2]).replace('\n','').replace(' ', '')
    #line[3] = str(line[3]).replace('\n','').replace(' ', '')
    #line[4] = str(line[4]).replace('\n', '').replace(' ', '')
    #line[5] = str(line[5]).replace('\n', '').replace(' ', '')
    #line[6] = str(line[6]).replace('\n', '').replace(' ', '')
    #line[7] = str(line[7]).replace('\n', '').replace(' ', '')
    #if line[8]=='':
    #    for i in type:
    #        try:
    #            if i.split('[}')[1] in line[9].replace('\n', '').replace(' ', ''):
    #                line[8]=i.split('[}')[0]
    #                break
    #            else:
    #                continue
    #        except:
    #            line[8] = str(line[8]).replace('\n', '').replace(' ', '')
    #else:
    #line[8] = str(line[8]).replace('\n', '').replace(' ', '')
    #line[9] = str(line[9]).replace('\n', '').replace(' ', '')
    #line[10] = str(line[10]).replace('\n', '').replace(' ', '')
    #line[11] = str(line[11]).replace('\n', '').replace(' ', '')
    #line[12] = str(line[12]).replace('\n', '').replace(' ', '')
    #line[13] = str(line[13]).replace('\n', '').replace(' ', '')
    #line[14] = str(line[14]).replace('\n', '').replace(' ', '')

    #if line[10]!='':
    #    time.sleep(1)
    #    lnglat=address.checkaddress(str(line[10]))
    #else:
    #    lnglat=" [} "


    #if line[4]=='' and line[5]=='':
    #if  line[5] == '':
    #    continue
    #try:
    #    if 'shop' in line[4] :
    #        line[4] = str(line[4]).replace('\n', '').replace(' ', '').split('/')[-1]
    #    elif line[4]=='':
    #        line[4]=line[4].replace('\n','').replace(' ', '')
    #    else:
    #        line[4] = line[4].replace('\n', '').replace(' ', '').split('/')[-2]
    #except:
    #     print(line)
    #line[4] = str(line[4]).replace('\n', '').replace(' ', '')
   # if 'http' in line[5]:
    #   line[5] = str(line[5]).replace('\n','').replace(' ', '').split('/')[-1]
    #else:
       #line[5] = str(line[5]).replace('\n', '').replace(' ', '')
    #   continue
    data='[}'.join(line) #+'[}'+lnglat
    with open('C:/Users/Administrator/Desktop/1102.txt', 'a', encoding='utf-8') as f:
          f.write(data)
          f.write('\n')
'''
'''
success = []
with open('C:/Users/Administrator/Desktop/meituanshopdata.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line)
        success.append(line.split('[}')[1].replace('\n', '').split('/')[-2].replace(' ', ''))

with open('C:/Users/Administrator/Desktop/shop_detail.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.split('[}')[6].replace(' ', '').replace('\n', '') !='':
            data='%s[%s[%s' %(line.split('[}')[0].replace(' ','').replace('\n',''), line.split('[}')[1].replace(' ', '').replace('\n', ''),line.split('[}')[6].replace(' ', '').replace('\n', ''))
            with open('C:/Users/Administrator/Desktop/test2333.txt', 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')
'''
'''
success=[]
with open('C:/Users/Administrator/Desktop/20171101.txt', 'r', encoding='utf-8') as f:
    for line in f:
        success.append(line.split('[}')[0].replace('\n', '').replace(' ', '').replace('\ufeff',''))

with open('C:/Users/Administrator/Desktop/20171031.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.split('[}')[0].replace('\n', '').replace(' ', '').replace('\ufeff','') not in success:
            if line.replace('\n','').split('[}')[9]!='':
                if '(' in line.split('[}')[10]:
                    add=line.split('[}')[10].split('(')[0]
                elif '（' in line.split('[}')[10]:
                    add=line.split('[}')[10].split('（')[0]
                else:
                    add = line.split('[}')[10]

                if '区' not in add:
                    coords=line.split('[}')[-1]+','+line.split('[}')[-2].replace('\n','')
                    district=address.checkcoords(coords)
                    tmpadd=add
                else:
                    district=add.split('区')[0]+'区'
                    tmpadd = add.split('区')[1]

                #print(tmpadd)
                if '街' in tmpadd:
                    street=tmpadd.split('街')[0]+'街'
                    street_number = tmpadd.split('街')[1]
                elif '路' in tmpadd:
                    street = tmpadd.split('路')[0] + '路'
                    street_number = tmpadd.split('路')[1]
                elif '巷子' in tmpadd:
                    street = tmpadd.split('巷子')[0] + '巷子'
                    street_number = tmpadd.split('巷子')[1]
                elif '巷' in tmpadd:
                    street = tmpadd.split('巷')[0] + '巷'
                    street_number = tmpadd.split('巷')[1]
                elif '段' in tmpadd:
                    street = tmpadd.split('段')[0] + '段'
                    street_number = tmpadd.split('段')[1]
                elif '大道' in tmpadd:
                    street = tmpadd.split('大道')[0] + '大道'
                    street_number = tmpadd.split('大道')[1]
                else:
                    street = ''
                    street_number = tmpadd


                data=line.replace('\n','')+'[}'+district+'[}'+street+'[}'+street_number
            else:
                data=line.replace('\n','')+'[}[}[}'
            with open('C:/Users/Administrator/Desktop/20171101.txt', 'a', encoding='utf-8') as f:
                f.write(data)
                f.write('\n')
'''