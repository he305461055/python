import time
import pandas
from collections import Counter
import json
import re
import mysql入库 as mysqltool

file_name='万年场'
'''
with open('C:/Users/Administrator/Desktop/美团外卖/shoplist_8_8.txt','r',encoding='utf-8') as f:
    for line in f:
        url = line.split('[}')[0]
        shopname = line.split('[}')[1]
        star = line.split('[}')[2]
        shopsold = line.split('[}')[3]
        shopright = line.split('[}')[4]
        if 'km' in shopright:
            shopright = str(float(shopright[0:len(shopright) - 2]) * 1000)
        elif 'm' in shopright:
            shopright = str(float(shopright[0:len(shopright) - 1]))
        else:
            shopright=shopright
        shoptime = line.split('[}')[5]
        sendprice = line.split('[}')[6]
        deliveryfee = line.split('[}')[7]
        name = line.split('[}')[8]
        shopdata = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' % (
        url, shopname, star, shopsold, shopright, shoptime, sendprice, deliveryfee,name)
        with open('C:/Users/Administrator/Desktop/美团外卖/shoplist_8_8_1.txt', 'a', encoding='utf-8') as f:
            f.write(shopdata)
            #f.write('\n')
'''
with open('C:/Users/Administrator/Desktop/美团外卖/shopdetail_%s.txt' %file_name,'r',encoding='utf-8') as f:
    for line in f:
        url = line.split('[}')[0]
        shopname = line.split('[}')[1]
        if '(' in shopname or ')' in shopname or '（' in shopname:
            continue
        phone = line.split('[}')[2]
        if ',' in phone:
            phone1= phone.split(',')[0]
            phone2 = phone.split(',')[1]
            try:
               phone3 = phone.split(',')[2]
            except:
                phone3 = ' '
        else:
            phone1=phone
            phone2=' '
            phone3=' '
        address = line.split('[}')[3]
        time = line.split('[}')[4]
        delivery = line.split('[}')[5]
        shopdata = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' % (
         url,shopname, phone1,phone2,phone3, address, time, delivery)
        with open('C:/Users/Administrator/Desktop/美团外卖/shopdetail_%s_1.txt' %file_name, 'a', encoding='utf-8') as f:
            f.write(shopdata)

sql='insert into shopdetail(url,shopname,phone1,phone2,phone3,address,time,delivery) values'
mysqltool.get_sql(sql,'shopdetail_%s' %file_name)
'''
list1=[]
list2=[]
with open ('C:/Users/Administrator/Desktop/step9-xzcd2-alldone.geojson','r',encoding='utf-8') as f:
    for line in f:
        if '"first_geohash"' in line:
           list1.append(line.split(':')[-1].replace('"','').replace(',','').replace('\n',''))
        elif '"oid"' in line:
           list2.append(line.split(':')[-1].replace('"', '').replace(',','').replace('\n',''))

list3=list(zip(list2,list1))

data2=[]
for i in list1:
    data2.append(i[1:7])
values_counts = Counter(data2)
elementslist=list(values_counts)

datalist=[]
with open('C:/Users/Administrator/Desktop/step9-xzcd2-alldone.geojson', 'r', encoding='utf-8') as f:
    a = f.read()
    # myjson = re.findall('\"type\": \"FeatureCollection\",(.*?),\"userTagCloudList\"', a)[0]
    for i in json.loads(a)['features']:
       datalist.append(i)

for i in elementslist:
    s='{"type": "FeatureCollection","features": ['
    with open('C:/Users/Administrator/Desktop/分类/' + i + '.txt', 'a', encoding='utf-8') as f:
        f.write(s)
    for j in datalist:
        j=str(j).replace("'",'"')
        k=re.findall('\"end_geohash\": \"(.*?)\",',j)[0]
        if str(i) in k[0:6]:
            with open('C:/Users/Administrator/Desktop/分类/' +i+'.txt','a',encoding='utf-8') as f:
                f.write(str(j).replace('None','null'))
                f.write(',')
    ss=']}'
    with open('C:/Users/Administrator/Desktop/分类/' + i + '.txt', 'a', encoding='utf-8') as f:
        f.write(ss)
'''