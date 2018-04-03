import requests
import time
import simplejson
import json
import re
import os
import shutil
import re

def checkaddress(adress):
    time.sleep(1)
    r = requests.get('http://api.map.baidu.com/geocoder?output=json&address=成都%s' %adress.replace(' ','').replace('\n',''))
    json_data=r.json()
    if json_data[u'status'] =='OK':
        try:
            lng=json_data[u'result'][u'location'][u'lng']
            lat=json_data[u'result'][u'location'][u'lat']
            data='%s[}%s'%(lng,lat)
        except:
            data = '%s[}%s' % ('', '')

        return data
        #with open('C:/Users/Administrator/Desktop/经纬度.txt', 'a', encoding='utf-8') as f:
        #    f.write(data)
        #    f.write('\n')

def checkcoords(coords):
    time.sleep(1)
    r=requests.get('http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=%s&output=json&pois=1&ak=OF3Mprh5kDnDxaq9BA9GIGVtyo1b6FFl' %coords)
    #print(simplejson.loads(r.text))
    #print(r.text)
    #try:
    json_data=re.findall('renderReverse&&renderReverse\((.*?})\)',r.text)[0]
    #print(json_data)
    json_data=json.loads(str(json_data))
    #json_data=r.json()
    if json_data['status']==0:
        district=json_data['result'][u'addressComponent'][u'district']
        #town = json_data['result']['addressComponent']['town']
        #street = json_data['result']['addressComponent']['street']
        #street_number = json_data['result']['addressComponent']['street_number']
        data=district
    else:
        data = ''

    return data

def copy_file(olddir,newdir,old,new):
    oldname=olddir+old
    newname=newdir+new
    shutil.copyfile(oldname, newname)

olddir1='D:/photo/首页图片/'
newdir1='D:/photo/首页图片1101/'

olddir2='D:/photo/美团资质1106/'
newdir2='D:/photo/美团资质/'

olddir3='D:/photo/环境图片/'
newdir3='D:/photo/环境图片1101/'
'''
hj=[]
with open('C:/Users/Administrator/Desktop/1102.txt', 'r', encoding='utf-8') as f:
    for line in f:
        hj.append(line.replace('\n',''))

with open('C:/Users/Administrator/Desktop/1101.txt', 'r', encoding='utf-8') as f:
    for line in f:
        tmp = []
        tmp1=[]
        if line.split('[}')[3]!='':
            newlogo=line.split('[}')[2]+'_logo.jpg'
            try:
              copy_file(olddir1,newdir1,line.split('[}')[3],newlogo)
            except:
              print('newlogo'+line.split('[}')[3])
              newlogo = ''
        else:
            newlogo=''

        if line.split('[}')[4].replace('\n','')!='':
            newbiz=line.split('[}')[2]+'_biz_photo.jpg'
            try:
              copy_file(olddir2, newdir2, line.split('[}')[4].replace('\n',''), newbiz)
            except:
                print('newbiz' + line.split('[}')[4].replace('\n',''))
                newbiz = ''
        else:
            newbiz=''

        #newhj=line.split('[}')[2]+'_photo.jpg'
        for i in hj:
           if line.split('[}')[1] in i:
               tmp.append(i.split('[}')[1])
        for j in tmp:
            newhj=line.split('[}')[2]+'_photo_%s.jpg' %tmp.index(j)
            try:
              copy_file(olddir3, newdir3,j, newhj)
            except:
              print(line.split('[}')[1])
            tmp1.append(newhj)
        data='%s[}%s[}%s[}%s' %(line.replace('\n',''),newlogo,newbiz,','.join(tmp1))
        with open('C:/Users/Administrator/Desktop/1103.txt', 'a', encoding='utf-8') as f:
            f.write(data)
            f.write('\n')


#$checkcoords('30.649976,104.114249')
'''

a='Beautiful, is; better*than\nugly'
# 四个分隔符为：,  ;  *  \n
x= re.split(',|; |\*|\n',a)
print(x)

'''
import xlrd
wb = xlrd.open_workbook('C:/Users/Administrator/Desktop/匹配20171102.xlsx')  # 打开文件
sh = wb.sheet_by_name('Sheet1')

sh = wb.sheet_by_index(0)  # 第一个表

sheetNames = wb.sheet_names()  # 查看包含的工作表

# 获得工作表的两种方法
sh = wb.sheet_by_index(0)
sh = wb.sheet_by_name(u'Sheet1')

# 单元格的值
cellA1 = sh.cell(0, 0)
cellA1Value = cellA1.value

# 第一列的值
columnValueList1 = sh.col_values(0)
columnValueList2 = sh.col_values(4)
columnValueList3 = sh.col_values(11)
columnValueList4 = sh.col_values(12)
columnValueList5 = sh.col_values(13)
columnValueList6 = sh.col_values(14)
columnValueList7 = sh.col_values(22)
columnValueList8 = sh.col_values(6)
columnValueList9 = sh.col_values(21)
unionlist=list(zip(columnValueList1,columnValueList2,columnValueList3,columnValueList4,columnValueList5,columnValueList6,columnValueList7,columnValueList8,columnValueList9))

shuziregex = "1[34578]\d{9}"

for line in unionlist:
    line=list(line)
    line[0] = str(line[0]).replace('\n','').replace(' ', '')
    if line[1]!='':
        try:
          line[1] = re.findall(shuziregex,str(line[1]).replace('\n', '').replace(' ', ''))[0]
        except:
          line[1] = str(line[1]).replace('\n', '').replace(' ', '')
    else:
        line[1] = str(line[1]).replace('\n', '').replace(' ', '')
    line[2] = str(line[2]).replace('\n', '').replace(' ', '')
    line[3] = str(line[3]).replace('\n', '').replace(' ', '')
    if line[4]!='':
       line[4] = str(line[4]).replace('\n', '').replace(' ', '').split(',')[0]
    else:
       line[4] = str(line[4]).replace('\n', '').replace(' ', '')
    time = str(line[5]).replace('\n', '').replace(' ', '').replace('周一至周日', '')
    if '午市' in time and '晚市' in time:
        time1=time[1:12]
        time2=time[14:]
    elif time=='':
        time1='00:00'
        time2='24:00'
    elif len(time.split('-'))==2:
        time1=time.split('-')[0]
        time2=time.split('-')[1]
    elif len(time.split('-'))!=2:
        time1=time[0:11]
        time2=time[11:]
    else:
        time1=time
        time2=time
    line[6] = str(line[6]).replace('\n', '').replace(' ', '')
    line[7] = str(line[7]).replace('\n', '').replace(' ', '')
    line[8] = str(line[8]).replace('\n', '').replace(' ', '')
    #line[9] = str(line[9]).replace('\n', '').replace(' ', '')
    data = '%s}%s}%s}%s}%s}%s}%s}%s}%s}%s' %(line[0],line[1],line[2],line[3],line[4],time1,time2,line[6],line[7],line[8])
    with open('C:/Users/Administrator/Desktop/20171102.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')
'''
#'''
shuziregex = "1\d{10}"
import xlrd
wb = xlrd.open_workbook('C:/Users/Administrator/Desktop/填充数据20171110.xlsx')  # 打开文件
sh = wb.sheet_by_name('1116')

sh = wb.sheet_by_index(0)  # 第一个表

sheetNames = wb.sheet_names()  # 查看包含的工作表

# 获得工作表的两种方法
sh = wb.sheet_by_index(0)
sh = wb.sheet_by_name(u'1116')

# 单元格的值
cellA1 = sh.cell(0, 0)
cellA1Value = cellA1.value

# 第一列的值
columnValueList1 = sh.col_values(0)
columnValueList2 = sh.col_values(7)
columnValueList3 = sh.col_values(7)
#columnValueList4 = sh.col_values(3)
#columnValueList5 = sh.col_values(9)
unionlist=list(zip(columnValueList1,columnValueList2,columnValueList3))
for line in unionlist:
    line=list(line)
    line[0] = str(line[0]).replace('\n','').replace(' ', '').replace('.0','')
    try:
      line[1] = re.findall(shuziregex,str(line[1]).replace('\n', '').replace(' ', ''))[0]
    except:
      line[1]=''
    #line[2] = str(line[2]).replace('\n', '').replace(' ', '')

    data = '%s}%s' % (line[0], line[1])
    with open('C:/Users/Administrator/Desktop/20171116.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')
#'''
'''
shuziregex = "1\d{10}"
zhuojiregex = "028-\d{8}|\d{8}"
list=[]
with open('C:/Users/Administrator/Desktop/meituandata1115.txt', 'r', encoding='utf-8') as f:
    for line in f:
         line=line.replace('\n', '')
         bb=re.sub(r'：',':',line.replace('\n','').split('[}')[5])
         ss=re.sub(r';|\(|\)|和|点|春季|冬季|秋季|夏季|非营业时段|晚|上|周|pm|am|、|早|午|晚|市|一|二|三|四|五|六|日|餐|下|上|茶|夜宵|,|；|凌晨|零晨|每天|中|全天|夜|次日|休息|，','',bb )
         aa = re.sub('至|到|一|~|_|～|－|~|〜|--|---|—|——|———|----', '-', ss)
         dd=re.sub(r'^:|^--|^-|--$|-$|-:', '', aa)
         if dd=='':
             dd='00:00-24:00'
         list.append('%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' %(line.split('[}')[0],line.split('[}')[2],line.split('[}')[3],line.split('[}')[4],dd,line.split('[}')[6],line.split('[}')[7],line.split('[}')[8]))

for i in list:
     id=i.split('[}')[0]
     name=i.split('[}')[1]
     address=i.split('[}')[2]

     if  '(' in address:
         add = address.split('(')[0]
     elif '（' in address:
         add = address.split('（')[0]
     else:
         add = address

     if '区' not in add:
         #coords = line.split('[}')[-1] + ',' + line.split('[}')[-2].replace('\n', '')
         #district = address.checkcoords(coords)
         tmpadd = add
     else:
         district = add.split('区')[0] + '区'
         tmpadd = add.split('区')[1]

     tmp=[]
         # print(tmpadd)
     if '街' in tmpadd:
         street = tmpadd.split('街')[0] + '街'
         street_number = ''.join(tmpadd.split('街')[1:])
     elif '路' in tmpadd:
         street = tmpadd.split('路')[0] + '路'
         street_number = ''.join(tmpadd.split('路')[1:])
     elif '巷子' in tmpadd:
         street = tmpadd.split('巷子')[0] + '巷子'
         street_number = ''.join(tmpadd.split('巷子')[1:])
     elif '巷' in tmpadd:
         street = tmpadd.split('巷')[0] + '巷'
         street_number = ''.join(tmpadd.split('巷')[1:])
     elif '段' in tmpadd:
         street = tmpadd.split('段')[0] + '段'
         street_number = ''.join(tmpadd.split('段')[1:])
     elif '大道' in tmpadd:
         street = tmpadd.split('大道')[0] + '大道'
         street_number = ''.join(tmpadd.split('大道')[1:])
     else:
         street = ''
         street_number = tmpadd

     try:
        phone = re.findall(shuziregex, str(i.split('[}')[3]).replace(' ', ''))[0]
     except:
        try:
            phone = re.findall(zhuojiregex, str(i.split('[}')[3]).replace(' ', ''))[0]
        except:
            phone = ''

     aa = i.split('[}')[4].replace('---','-').replace('——','-')
     time=re.sub('^:','',aa)
     if len(time)>5 and len(time)<12:
         time1 = aa.split('-')[0]
         time2 = aa.split('-')[0]
         #print('%s[}%s[}%s' %(i.split('[}')[0],time1,time2))
     elif len(time)<5:
         time1 = '00:00'
         time2 = '23:59'
         #print('%s[}%s[}%s' % (i.split('[}')[0], time1, time2))
     elif len(time)>20 and len(time)<24:
         time1 = time[0:11]
         time2 = re.sub('^:|^-','',time[11:])
         #print('%s[}%s[}%s' % (i.split('[}')[0], time1,time2))
     else:
         time1 = time[0:5]
         time2 = time[-5:]
         #print('%s[}%s[}%s' % (i.split('[}')[0], time1, time2))

     img=i.split('[}')[5].split('/')[-1].split('?')[0]
     if img != '':
         newbiz =re.sub(r'\||\*|\"|\（|\）','',i.split('[}')[1]+id[0:5]+ '_biz_photo.jpg').replace(' ','')
         #try:
         #   copy_file(olddir2, newdir2, img, newbiz)
         #except:
         #    print('newbiz' + img)
         #    newbiz = ''
     else:
         newbiz = ''

     type = i.split('[}')[6]
     iszz = i.split('[}')[7]

     try:
        phone1 = re.findall(shuziregex, str(i.split('[}')[3]).replace(' ', ''))[0]
     except:
        phone1 = ''

     data='%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' %(id,name,address,street,street_number,phone,time1,time2,newbiz,type,iszz,phone1)
     with open('C:/Users/Administrator/Desktop/20171116_0.txt', 'a', encoding='utf-8') as f:
         f.write(data)
         f.write('\n')
'''
#17:00-02:00